from database import SessionLocal
from models import Content
from langdetect import detect, LangDetectException
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def cleanup_non_english_content():
    db = SessionLocal()
    try:
        all_content = db.query(Content).all()
        total = len(all_content)
        removed = 0
        
        logger.info(f"Checking {total} articles for language...")
        
        for content in all_content:
            try:
                reader_text = content.reader_mode_content[:200] if content.reader_mode_content else ""
                combined_text = f"{content.title} {reader_text}"
                
                if len(combined_text.strip()) < 10:
                    continue
                
                detected_lang = detect(combined_text)
                
                if detected_lang != 'en':
                    logger.info(f"Removing non-English ({detected_lang}) content: {content.title[:60]}...")
                    db.delete(content)
                    removed += 1
                    
            except LangDetectException:
                logger.warning(f"Could not detect language for: {content.title[:60]}...")
                continue
            except Exception as e:
                logger.error(f"Error processing content {content.id}: {str(e)}")
                continue
        
        db.commit()
        logger.info(f"\nCleanup completed!")
        logger.info(f"Total articles checked: {total}")
        logger.info(f"Non-English articles removed: {removed}")
        logger.info(f"English articles remaining: {total - removed}")
        
    except Exception as e:
        logger.error(f"Cleanup failed: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    cleanup_non_english_content()

