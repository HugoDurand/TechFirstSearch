from database import SessionLocal
from models import Content
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


TRACKING_PARAMS = {
    'source', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term',
    'fbclid', 'gclid', 'ref', 'mc_cid', 'mc_eid', '_ga', 'campaign_id'
}


def normalize_url(url: str) -> str:
    try:
        parsed = urlparse(url)
        
        if parsed.query:
            params = parse_qs(parsed.query)
            cleaned_params = {
                k: v for k, v in params.items()
                if k.lower() not in TRACKING_PARAMS
            }
            
            cleaned_query = urlencode(cleaned_params, doseq=True) if cleaned_params else ''
            
            normalized = urlunparse((
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                cleaned_query,
                ''
            ))
        else:
            normalized = urlunparse((
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                parsed.query,
                ''
            ))
        
        normalized = normalized.rstrip('/')
        
        return normalized
        
    except Exception as e:
        logger.warning(f"Failed to normalize URL {url}: {str(e)}")
        return url


def cleanup_duplicates():
    db = SessionLocal()
    try:
        all_content = db.query(Content).all()
        total = len(all_content)
        
        logger.info(f"Checking {total} articles for duplicates...")
        
        url_map = {}
        duplicates_to_remove = []
        
        for content in all_content:
            normalized = normalize_url(content.url)
            
            if normalized in url_map:
                existing_content = url_map[normalized]
                logger.info(
                    f"Found duplicate: '{content.title[:60]}...'\n"
                    f"  Keeping:  ID={existing_content.id}, Source={existing_content.source_name}\n"
                    f"  Removing: ID={content.id}, Source={content.source_name}"
                )
                duplicates_to_remove.append(content)
            else:
                url_map[normalized] = content
                if normalized != content.url:
                    logger.info(f"Normalizing URL for ID={content.id}: {content.url[:80]}...")
                    content.url = normalized
        
        logger.info(f"\nRemoving {len(duplicates_to_remove)} duplicate articles...")
        
        for duplicate in duplicates_to_remove:
            db.delete(duplicate)
        
        db.commit()
        
        logger.info(f"\nCleanup completed!")
        logger.info(f"Total articles checked: {total}")
        logger.info(f"Duplicates removed: {len(duplicates_to_remove)}")
        logger.info(f"Unique articles remaining: {len(url_map)}")
        
    except Exception as e:
        logger.error(f"Cleanup failed: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    cleanup_duplicates()

