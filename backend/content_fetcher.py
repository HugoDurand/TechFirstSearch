import feedparser
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
import re
from sqlalchemy.orm import Session
from langdetect import detect, LangDetectException
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

from models import Content, Source
from database import SessionLocal

logger = logging.getLogger(__name__)

BROWSER_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}


class ArxivURLConverter:
    @staticmethod
    def is_arxiv_url(url: str) -> bool:
        return 'arxiv.org' in url
    
    @staticmethod
    def get_arxiv_id(url: str) -> Optional[str]:
        patterns = [
            r'arxiv\.org/abs/(\d+\.\d+)',
            r'arxiv\.org/pdf/(\d+\.\d+)',
            r'arxiv\.org/html/(\d+\.\d+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    @staticmethod
    def to_html_url(url: str) -> str:
        arxiv_id = ArxivURLConverter.get_arxiv_id(url)
        if arxiv_id:
            return f'https://arxiv.org/html/{arxiv_id}v1'
        return url
    
    @staticmethod
    def to_abs_url(url: str) -> str:
        arxiv_id = ArxivURLConverter.get_arxiv_id(url)
        if arxiv_id:
            return f'https://arxiv.org/abs/{arxiv_id}'
        return url


class URLNormalizer:
    TRACKING_PARAMS = {
        'source', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term',
        'fbclid', 'gclid', 'ref', 'mc_cid', 'mc_eid', '_ga', 'campaign_id'
    }
    
    @staticmethod
    def normalize(url: str) -> str:
        try:
            parsed = urlparse(url)
            
            if parsed.query:
                params = parse_qs(parsed.query)
                cleaned_params = {
                    k: v for k, v in params.items()
                    if k.lower() not in URLNormalizer.TRACKING_PARAMS
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


class LanguageFilter:
    @staticmethod
    def is_english(text: str, min_length: int = 30) -> bool:
        if not text or len(text.strip()) < 10:
            return False
        
        try:
            cleaned_text = text.strip()
            
            non_latin_chars = sum(1 for c in cleaned_text if ord(c) > 0x024F)
            total_chars = len(cleaned_text.replace(' ', ''))
            
            if total_chars > 0 and (non_latin_chars / total_chars) > 0.3:
                return False
            
            if len(cleaned_text) < min_length:
                return True
            
            detected_lang = detect(cleaned_text)
            return detected_lang == 'en'
        except LangDetectException:
            logger.debug(f"Could not detect language for text: {text[:50]}...")
            return True
    
    @staticmethod
    def filter_content(title: str, summary: str = "") -> bool:
        if summary and len(summary) > 50:
            combined_text = f"{title} {summary}"
            return LanguageFilter.is_english(combined_text, min_length=60)
        else:
            return LanguageFilter.is_english(title, min_length=50)


class ContentClassifier:
    @staticmethod
    def classify(title: str, source_name: str, tags: Optional[List[str]] = None) -> str:
        title_lower = title.lower()
        tags_lower = [tag.lower() for tag in (tags or [])]
        source_lower = source_name.lower()
        
        academic_sources = ['arxiv', 'papers with code', 'acm', 'ieee', 'scholar']
        if any(src in source_lower for src in academic_sources):
            return 'paper'
        
        if 'research' in source_lower or 'research' in title_lower:
            return 'research'
        
        news_sources = ['techcrunch', 'ars technica', 'the verge', 'wired', 'hacker news']
        if any(src in source_lower for src in news_sources):
            return 'news'
        
        tutorial_keywords = ['tutorial', 'how-to', 'guide', 'how to', 'step by step']
        if any(keyword in title_lower for keyword in tutorial_keywords):
            return 'tutorial'
        if any(keyword in tags_lower for keyword in tutorial_keywords):
            return 'tutorial'
        
        essay_sources = ['medium', 'substack']
        if any(src in source_lower for src in essay_sources):
            return 'essay'
        
        post_sources = ['dev.to', 'hashnode', 'reddit']
        if any(src in source_lower for src in post_sources):
            return 'post'
        
        return 'article'


class ReaderModeExtractor:
    @staticmethod
    def fix_relative_urls(html_content: str, base_url: str) -> str:
        """Convert relative URLs to absolute URLs in HTML content"""
        try:
            from urllib.parse import urljoin, urlparse
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Get base domain
            parsed_base = urlparse(base_url)
            base_domain = f"{parsed_base.scheme}://{parsed_base.netloc}"
            
            # Fix img src attributes
            for img in soup.find_all('img'):
                src = img.get('src')
                if src and not src.startswith(('http://', 'https://', 'data:')):
                    img['src'] = urljoin(base_domain, src)
                
                # Also fix data-src for lazy-loaded images
                data_src = img.get('data-src')
                if data_src and not data_src.startswith(('http://', 'https://', 'data:')):
                    img['data-src'] = urljoin(base_domain, data_src)
            
            # Fix a href attributes
            for a in soup.find_all('a'):
                href = a.get('href')
                if href and not href.startswith(('http://', 'https://', 'mailto:', 'tel:', '#', 'javascript:')):
                    a['href'] = urljoin(base_domain, href)
            
            # Fix source src attributes (for video/picture elements)
            for source in soup.find_all('source'):
                src = source.get('src')
                if src and not src.startswith(('http://', 'https://', 'data:')):
                    source['src'] = urljoin(base_domain, src)
            
            return str(soup)
        except Exception as e:
            logger.warning(f"Failed to fix relative URLs: {e}")
            return html_content
    
    @staticmethod
    def extract(url: str) -> tuple[Optional[str], Optional[str], Optional[str]]:
        try:
            from readability import Document
            import requests
            from bs4 import BeautifulSoup
            
            # For ArXiv, use the HTML version for better content extraction
            fetch_url = url
            if ArxivURLConverter.is_arxiv_url(url):
                fetch_url = ArxivURLConverter.to_html_url(url)
                logger.info(f"ArXiv detected, using HTML version: {fetch_url}")
            
            # Fetch the HTML content with browser-like headers
            response = requests.get(fetch_url, timeout=10, headers=BROWSER_HEADERS)
            response.raise_for_status()
            html_content = response.text
            
            # Use readability to extract the main content HTML
            doc = Document(html_content)
            clean_html = doc.summary()
            
            # Extract featured image if present
            original_soup = BeautifulSoup(html_content, 'html.parser')
            featured_image = None
            featured_image_url = None
            
            # Try to find the featured/hero image from the original HTML
            og_image = original_soup.find('meta', property='og:image')
            if og_image and og_image.get('content'):
                featured_image_url = og_image['content']
                # Check if this image is not already in the cleaned content
                if featured_image_url not in clean_html:
                    featured_image = f'<figure class="featured-image"><img src="{featured_image_url}" alt="{doc.title()}" /></figure>'
            
            # Further clean the HTML to remove navigation, menus, and non-article content
            soup = BeautifulSoup(clean_html, 'html.parser')
            
            # Remove navigation and structural elements
            for tag in soup.find_all(['nav', 'header', 'footer', 'aside', 'menu']):
                tag.decompose()
            
            # Remove elements with clear navigation/structural classes and IDs
            # Only use obvious, universally applicable patterns
            unwanted_keywords = [
                'nav', 'menu', 'sidebar', 'header', 'footer', 'banner',
                'advertisement', 'ad-', 'social-', 'share-',
                'newsletter', 'subscribe', 'signup', 'promo'
            ]
            
            for tag in soup.find_all(attrs={'class': True}):
                classes = ' '.join(tag.get('class', [])).lower()
                if any(keyword in classes for keyword in unwanted_keywords):
                    tag.decompose()
            
            for tag in soup.find_all(attrs={'id': True}):
                tag_id = tag.get('id', '').lower()
                if any(keyword in tag_id for keyword in unwanted_keywords):
                    tag.decompose()
            
            # Remove "Skip to" links (common in accessibility navigation)
            for a_tag in soup.find_all('a'):
                link_text = a_tag.get_text(strip=True).lower()
                if link_text.startswith('skip to') or link_text.startswith('skip '):
                    a_tag.decompose()
            
            # STRUCTURAL CLEANING: Remove sections based on link density and patterns
            
            # 0. Identify and isolate main article content (site-specific patterns)
            # Some sites use data-testid or other markers to denote article sections
            article_markers = soup.find_all(attrs={'data-testid': lambda x: x and 'companionColumn' in x})
            if article_markers:
                # Find the last article section
                last_article_marker = article_markers[-1]
                
                # Remove everything after the last article marker
                current = last_article_marker
                while current:
                    next_sibling = current.find_next_sibling()
                    if next_sibling:
                        # Check if this sibling is also part of article
                        if not (next_sibling.get('data-testid') and 'companionColumn' in next_sibling.get('data-testid', '')):
                            next_sibling.decompose()
                    current = next_sibling
                
                # Also remove any parent's siblings that come after
                article_parent = last_article_marker.parent
                if article_parent:
                    for sibling in list(article_parent.find_next_siblings()):
                        sibling.decompose()
            
            # 1. Remove sections with high link-to-text ratio (likely navigation/recommendations)
            for section in soup.find_all(['div', 'section', 'aside']):
                text_content = section.get_text(strip=True)
                links = section.find_all('a')
                
                if text_content and len(text_content) > 0:
                    # Calculate link density
                    link_text_length = sum(len(link.get_text(strip=True)) for link in links)
                    total_text_length = len(text_content)
                    link_density = link_text_length / total_text_length if total_text_length > 0 else 0
                    
                    # If section is >70% links and has multiple short links, it's likely navigation
                    if link_density > 0.7 and len(links) > 3:
                        avg_link_length = link_text_length / len(links) if len(links) > 0 else 0
                        if avg_link_length < 50:  # Short links = navigation
                            section.decompose()
                            continue
            
            # 2. Remove lists where all items are just links (navigation pattern)
            for ul_tag in soup.find_all(['ul', 'ol']):
                items = ul_tag.find_all('li', recursive=False)
                if not items:
                    ul_tag.decompose()
                    continue
                
                # Check if this looks like a navigation list
                link_only_items = 0
                for li in items:
                    li_text = li.get_text(strip=True)
                    li_links = li.find_all('a')
                    
                    # Item is "link-only" if it has links and minimal non-link text
                    if li_links:
                        link_text = ''.join(link.get_text(strip=True) for link in li_links)
                        if len(li_text) > 0 and len(link_text) / len(li_text) > 0.8:
                            link_only_items += 1
                
                # If most items are link-only, remove the list
                if link_only_items >= len(items) * 0.8:
                    ul_tag.decompose()
            
            # 3. Remove standalone links not within meaningful content
            for a_tag in soup.find_all('a'):
                # Keep links that are inside paragraphs, list items, blockquotes
                if a_tag.find_parent(['p', 'blockquote', 'td', 'li']):
                    continue
                
                # Keep links with images
                if a_tag.find('img'):
                    continue
                
                # Remove standalone navigation links
                a_tag.decompose()
            
            # 4. Remove elements that look like "tags" or "categories" (multiple short links in a row)
            for parent in soup.find_all(['p', 'div', 'span']):
                links = parent.find_all('a', recursive=False)
                if len(links) >= 3:
                    # If parent has 3+ direct child links and little other text
                    parent_text = parent.get_text(strip=True)
                    link_text = ''.join(link.get_text(strip=True) for link in links)
                    
                    if len(parent_text) > 0 and len(link_text) / len(parent_text) > 0.7:
                        # Check if links are short (tag-like)
                        avg_link_len = len(link_text) / len(links)
                        if avg_link_len < 30:
                            parent.decompose()
            
            # 5. Remove empty elements
            for tag in soup.find_all(['p', 'div', 'span', 'section', 'li']):
                if not tag.get_text(strip=True) and not tag.find(['img', 'figure', 'video', 'iframe']):
                    tag.decompose()
            
            # Inject featured image at the beginning if found
            if featured_image:
                body = soup.find('body')
                if body and body.find():
                    first_content = body.find()
                    featured_soup = BeautifulSoup(featured_image, 'html.parser')
                    first_content.insert_before(featured_soup)
            
            # Get the cleaned HTML
            clean_html = str(soup)
            
            # Convert relative URLs to absolute URLs
            clean_html = ReaderModeExtractor.fix_relative_urls(clean_html, fetch_url)
            
            # Also use Newspaper3k for plain text extraction
            article = Article(url)
            article.download()
            article.parse()
            reader_content = article.text
            
            return clean_html, reader_content, featured_image_url
        except Exception as e:
            logger.error(f"Failed to extract content from {url}: {str(e)}")
            return None, None, None


class ImageExtractor:
    @staticmethod
    def extract_from_html(html_content: str) -> Optional[str]:
        """Extract image URL from HTML content (works with raw or cleaned HTML)"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Try Open Graph image
            og_image = soup.find('meta', property='og:image')
            if og_image and og_image.get('content'):
                return og_image.get('content')
            
            # Try Twitter Card image (with property)
            twitter_image = soup.find('meta', property='twitter:image')
            if twitter_image and twitter_image.get('content'):
                return twitter_image.get('content')
            
            # Try Twitter Card image (with name attribute)
            twitter_image_alt = soup.find('meta', attrs={'name': 'twitter:image'})
            if twitter_image_alt and twitter_image_alt.get('content'):
                return twitter_image_alt.get('content')
            
            # Try featured/hero figure
            featured = soup.find('figure', class_=re.compile(r'featured|hero|article|wp-block-image'))
            if featured:
                img = featured.find('img')
                if img:
                    src = img.get('src') or img.get('data-src')
                    if src and src.startswith('http'):
                        return src
            
            # Try first image in article
            article_section = soup.find(['article', 'main', 'div'], class_=re.compile(r'article|post|content'))
            if article_section:
                img = article_section.find('img')
                if img:
                    src = img.get('src') or img.get('data-src')
                    if src and src.startswith('http'):
                        return src
            
            # Fallback: find any img tag with http URL (for RSS content)
            for img in soup.find_all('img'):
                src = img.get('src') or img.get('data-src')
                if src and src.startswith('http'):
                    # Skip tiny tracking pixels
                    width = img.get('width', '999')
                    height = img.get('height', '999')
                    try:
                        if int(width) > 10 and int(height) > 10:
                            return src
                    except (ValueError, TypeError):
                        return src
            
            return None
        except Exception as e:
            logger.warning(f"Failed to extract image from HTML: {e}")
            return None
    
    @staticmethod
    def extract_from_url(url: str) -> Optional[str]:
        """Extract image URL by fetching and parsing the URL"""
        try:
            # For ArXiv, use the HTML version for better image extraction
            fetch_url = url
            if ArxivURLConverter.is_arxiv_url(url):
                fetch_url = ArxivURLConverter.to_html_url(url)
            
            response = requests.get(fetch_url, timeout=5, headers=BROWSER_HEADERS)
            return ImageExtractor.extract_from_html(response.text)
        except Exception as e:
            logger.debug(f"Could not extract image from {url}: {str(e)}")
            return None


class RSSFetcher:
    @staticmethod
    def fetch(feed_url: str, source_name: str) -> List[Dict]:
        try:
            feed = feedparser.parse(feed_url)
            items = []
            
            for entry in feed.entries:
                published_date = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published_date = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    published_date = datetime(*entry.updated_parsed[:6])
                else:
                    published_date = datetime.now()
                
                thumbnail = None
                if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                    thumbnail = entry.media_thumbnail[0]['url']
                elif hasattr(entry, 'media_content') and entry.media_content:
                    thumbnail = entry.media_content[0]['url']
                
                if not thumbnail:
                    content_html = ''
                    if hasattr(entry, 'content') and entry.content:
                        content_html = entry.content[0].get('value', '')
                    elif hasattr(entry, 'summary'):
                        content_html = entry.summary
                    
                    if content_html:
                        thumbnail = ImageExtractor.extract_from_html(content_html)
                
                if not thumbnail:
                    thumbnail = ImageExtractor.extract_from_url(entry.link)
                
                tags = []
                if hasattr(entry, 'tags'):
                    tags = [tag.term for tag in entry.tags]
                
                summary = entry.summary if hasattr(entry, 'summary') else ""
                
                if not LanguageFilter.filter_content(entry.title, summary):
                    logger.info(f"Filtered non-English content: {entry.title[:60]}...")
                    continue
                
                items.append({
                    'title': entry.title,
                    'url': entry.link,
                    'source_name': source_name,
                    'published_date': published_date,
                    'thumbnail_url': thumbnail,
                    'author': entry.author if hasattr(entry, 'author') else None,
                    'tags': tags
                })
            
            return items
        except Exception as e:
            logger.error(f"Failed to fetch RSS from {feed_url}: {str(e)}")
            return []


class HackerNewsFetcher:
    @staticmethod
    def fetch() -> List[Dict]:
        try:
            response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json', timeout=10)
            response.raise_for_status()
            story_ids = response.json()[:50]
            
            items = []
            for story_id in story_ids:
                try:
                    story_response = requests.get(
                        f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json',
                        timeout=5
                    )
                    story = story_response.json()
                    
                    if story and story.get('url'):
                        title = story.get('title')
                        if not LanguageFilter.is_english(title):
                            logger.info(f"Filtered non-English HN content: {title[:60]}...")
                            continue
                        
                        items.append({
                            'title': title,
                            'url': story.get('url'),
                            'source_name': 'Hacker News',
                            'published_date': datetime.fromtimestamp(story.get('time')),
                            'thumbnail_url': None,
                            'author': story.get('by'),
                            'tags': []
                        })
                except Exception as e:
                    logger.error(f"Failed to fetch HN story {story_id}: {str(e)}")
                    continue
            
            return items
        except Exception as e:
            logger.error(f"Failed to fetch Hacker News: {str(e)}")
            return []


class DevToFetcher:
    @staticmethod
    def fetch() -> List[Dict]:
        try:
            response = requests.get(
                'https://dev.to/api/articles',
                params={'per_page': 50},
                timeout=10
            )
            response.raise_for_status()
            articles = response.json()
            
            items = []
            for article in articles:
                title = article.get('title')
                description = article.get('description', '')
                
                if not LanguageFilter.filter_content(title, description):
                    logger.info(f"Filtered non-English Dev.to content: {title[:60]}...")
                    continue
                
                items.append({
                    'title': title,
                    'url': article.get('url'),
                    'source_name': 'Dev.to',
                    'published_date': datetime.fromisoformat(
                        article.get('published_at').replace('Z', '+00:00')
                    ),
                    'thumbnail_url': article.get('cover_image'),
                    'author': article.get('user', {}).get('name'),
                    'tags': article.get('tag_list', [])
                })
            
            return items
        except Exception as e:
            logger.error(f"Failed to fetch Dev.to: {str(e)}")
            return []


class ContentAggregator:
    def __init__(self, db: Session):
        self.db = db
    
    def fetch_all_sources(self):
        sources = self.db.query(Source).filter(Source.is_active == True).all()
        
        all_items = []
        for source in sources:
            logger.info(f"Fetching from {source.name}")
            
            try:
                if source.source_type == 'RSS' and source.feed_url:
                    items = RSSFetcher.fetch(source.feed_url, source.name)
                    all_items.extend(items)
                elif source.source_type == 'API':
                    if 'hacker' in source.name.lower():
                        items = HackerNewsFetcher.fetch()
                        all_items.extend(items)
                    elif 'dev.to' in source.name.lower():
                        items = DevToFetcher.fetch()
                        all_items.extend(items)
                
                source.last_fetched = datetime.now()
                self.db.commit()
                
            except Exception as e:
                logger.error(f"Failed to fetch from {source.name}: {str(e)}")
                continue
        
        self.process_and_store(all_items)
    
    def process_and_store(self, items: List[Dict]):
        for item in items:
            try:
                normalized_url = URLNormalizer.normalize(item['url'])
                
                existing = self.db.query(Content).filter(
                    Content.url == normalized_url
                ).first()
                
                if existing:
                    logger.debug(f"Skipping duplicate: {item['title'][:60]}...")
                    continue
                
                item['url'] = normalized_url
                
                content_type = ContentClassifier.classify(
                    item['title'],
                    item['source_name'],
                    item.get('tags')
                )
                
                full_content, reader_content, extracted_image_url = ReaderModeExtractor.extract(item['url'])
                
                # Use extracted featured image if no thumbnail was provided
                thumbnail_url = item.get('thumbnail_url')
                if not thumbnail_url and extracted_image_url:
                    thumbnail_url = extracted_image_url
                
                author = item.get('author', '')
                if author and len(author) > 200:
                    author = author[:197] + '...'
                
                title = item['title']
                if title and len(title) > 500:
                    title = title[:497] + '...'
                
                ai_summary = None
                ai_key_points = None
                
                try:
                    from ai_summarizer import generate_article_summary
                    text_for_summary = reader_content or full_content
                    ai_summary, ai_key_points = generate_article_summary(
                        title, 
                        text_for_summary, 
                        item['source_name']
                    )
                except Exception as e:
                    logger.warning(f"Failed to generate AI summary: {str(e)}")
                
                content = Content(
                    title=title,
                    url=item['url'],
                    source_name=item['source_name'],
                    content_type=content_type,
                    published_date=item['published_date'],
                    thumbnail_url=thumbnail_url[:2048] if thumbnail_url else None,
                    author=author if author else None,
                    tags=item.get('tags'),
                    full_content=full_content,
                    reader_mode_content=reader_content,
                    ai_summary=ai_summary,
                    ai_key_points=ai_key_points
                )
                
                self.db.add(content)
                self.db.commit()
                logger.info(f"Added content: {item['title']}")
                
            except Exception as e:
                logger.error(f"Failed to process item {item.get('url')}: {str(e)}")
                self.db.rollback()
                continue


def run_content_fetch():
    db = SessionLocal()
    try:
        aggregator = ContentAggregator(db)
        aggregator.fetch_all_sources()
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_content_fetch()

