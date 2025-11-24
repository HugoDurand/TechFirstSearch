from database import SessionLocal, init_db
from models import Source
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_sources():
    init_db()
    db = SessionLocal()
    
    sources = [
        {
            'name': 'Hacker News',
            'url': 'https://news.ycombinator.com',
            'source_type': 'API',
            'feed_url': None
        },
        {
            'name': 'Dev.to',
            'url': 'https://dev.to',
            'source_type': 'API',
            'feed_url': None
        },
        {
            'name': 'TechCrunch',
            'url': 'https://techcrunch.com',
            'source_type': 'RSS',
            'feed_url': 'https://techcrunch.com/feed/'
        },
        {
            'name': 'Ars Technica',
            'url': 'https://arstechnica.com',
            'source_type': 'RSS',
            'feed_url': 'https://feeds.arstechnica.com/arstechnica/index'
        },
        {
            'name': 'The Verge',
            'url': 'https://www.theverge.com',
            'source_type': 'RSS',
            'feed_url': 'https://www.theverge.com/rss/index.xml'
        },
        {
            'name': 'GitHub Blog',
            'url': 'https://github.blog',
            'source_type': 'RSS',
            'feed_url': 'https://github.blog/feed/'
        },
        {
            'name': 'Stack Overflow Blog',
            'url': 'https://stackoverflow.blog',
            'source_type': 'RSS',
            'feed_url': 'https://stackoverflow.blog/feed/'
        },
        {
            'name': 'FreeCodeCamp',
            'url': 'https://www.freecodecamp.org/news',
            'source_type': 'RSS',
            'feed_url': 'https://www.freecodecamp.org/news/rss/'
        },
        {
            'name': 'MIT Technology Review',
            'url': 'https://www.technologyreview.com',
            'source_type': 'RSS',
            'feed_url': 'https://www.technologyreview.com/feed/'
        },
        {
            'name': 'Wired',
            'url': 'https://www.wired.com',
            'source_type': 'RSS',
            'feed_url': 'https://www.wired.com/feed/rss'
        },
        {
            'name': 'CNN Business Tech',
            'url': 'https://www.cnn.com/business/tech',
            'source_type': 'RSS',
            'feed_url': 'https://www.cnn.com/services/rss/technology/'
        },
        {
            'name': 'CNBC Technology',
            'url': 'https://www.cnbc.com/technology/',
            'source_type': 'RSS',
            'feed_url': 'https://www.cnbc.com/id/19854910/device/rss/rss.html'
        },
        {
            'name': 'Ontologist',
            'url': 'https://ontologist.substack.com',
            'source_type': 'RSS',
            'feed_url': 'https://ontologist.substack.com/feed'
        },
        {
            'name': 'LinkedIn Engineering',
            'url': 'https://www.linkedin.com/blog/engineering',
            'source_type': 'RSS',
            'feed_url': 'https://engineering.linkedin.com/blog.rss.html'
        },
        {
            'name': 'Dropbox Tech',
            'url': 'https://dropbox.tech',
            'source_type': 'RSS',
            'feed_url': 'https://dropbox.tech/feed'
        },
        {
            'name': 'Business Insider Tech',
            'url': 'https://www.businessinsider.com/tech',
            'source_type': 'RSS',
            'feed_url': 'https://www.businessinsider.com/sai/rss'
        },
        {
            'name': 'Tom Tunguz',
            'url': 'https://tomtunguz.com',
            'source_type': 'RSS',
            'feed_url': 'https://tomtunguz.com/rss/'
        },
        {
            'name': 'Fidjisimo',
            'url': 'https://fidjisimo.substack.com',
            'source_type': 'RSS',
            'feed_url': 'https://fidjisimo.substack.com/feed'
        },
        {
            'name': 'Cline Bot Blog',
            'url': 'https://cline.bot/blog',
            'source_type': 'RSS',
            'feed_url': 'https://cline.bot/blog/feed'
        },
        {
            'name': 'Theory VC',
            'url': 'https://theoryvc.com/blog',
            'source_type': 'RSS',
            'feed_url': 'https://theoryvc.com/blog/feed'
        },
        {
            'name': 'The Letter Two',
            'url': 'https://thelettertwo.com/blog/',
            'source_type': 'RSS',
            'feed_url': 'https://thelettertwo.com/blog/feed'
        },
        {
            'name': '9to5Mac',
            'url': 'https://9to5mac.com',
            'source_type': 'RSS',
            'feed_url': 'https://9to5mac.com/feed/'
        },
        {
            'name': 'Anthropic Engineering',
            'url': 'https://www.anthropic.com/engineering',
            'source_type': 'RSS',
            'feed_url': 'https://www.anthropic.com/engineering/rss.xml'
        },
        {
            'name': 'Anthropic News',
            'url': 'https://www.anthropic.com/news',
            'source_type': 'RSS',
            'feed_url': 'https://www.anthropic.com/news/rss.xml'
        },
        {
            'name': 'OpenAI News',
            'url': 'https://openai.com/news/',
            'source_type': 'RSS',
            'feed_url': 'https://openai.com/news/rss.xml'
        },
        {
            'name': 'Every.to',
            'url': 'https://every.to',
            'source_type': 'RSS',
            'feed_url': 'https://every.to/feed'
        },
        {
            'name': 'Medium Engineering',
            'url': 'https://medium.engineering',
            'source_type': 'RSS',
            'feed_url': 'https://medium.engineering/feed'
        },
        {
            'name': 'Medium - AI',
            'url': 'https://medium.com/tag/artificial-intelligence',
            'source_type': 'RSS',
            'feed_url': 'https://medium.com/feed/tag/artificial-intelligence'
        },
        {
            'name': 'Medium - Technology',
            'url': 'https://medium.com/tag/technology',
            'source_type': 'RSS',
            'feed_url': 'https://medium.com/feed/tag/technology'
        },
        {
            'name': 'Medium - Programming',
            'url': 'https://medium.com/tag/programming',
            'source_type': 'RSS',
            'feed_url': 'https://medium.com/feed/tag/programming'
        },
        {
            'name': 'Medium - Data Science',
            'url': 'https://medium.com/tag/data-science',
            'source_type': 'RSS',
            'feed_url': 'https://medium.com/feed/tag/data-science'
        },
        {
            'name': 'Meta Engineering',
            'url': 'https://engineering.fb.com',
            'source_type': 'RSS',
            'feed_url': 'https://engineering.fb.com/feed/'
        },
        {
            'name': 'Meta AI',
            'url': 'https://ai.meta.com/blog/',
            'source_type': 'RSS',
            'feed_url': 'https://ai.meta.com/blog/feed/'
        },
        {
            'name': 'Google Blog',
            'url': 'https://blog.google',
            'source_type': 'RSS',
            'feed_url': 'https://blog.google/rss/'
        },
        {
            'name': 'Rochester News',
            'url': 'https://www.rochester.edu/newscenter/',
            'source_type': 'RSS',
            'feed_url': 'https://www.rochester.edu/newscenter/feed/'
        },
        {
            'name': 'Perspectiveship',
            'url': 'https://read.perspectiveship.com',
            'source_type': 'RSS',
            'feed_url': 'https://read.perspectiveship.com/feed'
        },
        {
            'name': 'Human Invariant',
            'url': 'https://humaninvariant.substack.com',
            'source_type': 'RSS',
            'feed_url': 'https://humaninvariant.substack.com/feed'
        },
        {
            'name': 'The Register',
            'url': 'https://www.theregister.com',
            'source_type': 'RSS',
            'feed_url': 'https://www.theregister.com/headlines.atom'
        },
        {
            'name': 'Piccalilli',
            'url': 'https://piccalil.li/blog/',
            'source_type': 'RSS',
            'feed_url': 'https://piccalil.li/feed.xml'
        },
        {
            'name': 'Nextword',
            'url': 'https://nextword.substack.com',
            'source_type': 'RSS',
            'feed_url': 'https://nextword.substack.com/feed'
        },
        {
            'name': 'Read Write Rachel',
            'url': 'https://www.readwriterachel.com',
            'source_type': 'RSS',
            'feed_url': 'https://www.readwriterachel.com/feed'
        },
        {
            'name': 'ArXiv - AI',
            'url': 'https://arxiv.org/list/cs.AI/recent',
            'source_type': 'RSS',
            'feed_url': 'https://rss.arxiv.org/rss/cs.AI'
        },
        {
            'name': 'ArXiv - Machine Learning',
            'url': 'https://arxiv.org/list/cs.LG/recent',
            'source_type': 'RSS',
            'feed_url': 'https://rss.arxiv.org/rss/cs.LG'
        },
        {
            'name': 'ArXiv - Computer Vision',
            'url': 'https://arxiv.org/list/cs.CV/recent',
            'source_type': 'RSS',
            'feed_url': 'https://rss.arxiv.org/rss/cs.CV'
        },
        {
            'name': 'ArXiv - NLP',
            'url': 'https://arxiv.org/list/cs.CL/recent',
            'source_type': 'RSS',
            'feed_url': 'https://rss.arxiv.org/rss/cs.CL'
        },
        {
            'name': 'ArXiv - Robotics',
            'url': 'https://arxiv.org/list/cs.RO/recent',
            'source_type': 'RSS',
            'feed_url': 'https://rss.arxiv.org/rss/cs.RO'
        },
        {
            'name': 'ArXiv - ML Stats',
            'url': 'https://arxiv.org/list/stat.ML/recent',
            'source_type': 'RSS',
            'feed_url': 'https://rss.arxiv.org/rss/stat.ML'
        },
        {
            'name': 'Machine Learning Mastery',
            'url': 'https://machinelearningmastery.com/blog/',
            'source_type': 'RSS',
            'feed_url': 'https://machinelearningmastery.com/blog/feed/'
        },
        {
            'name': 'BAIR Blog',
            'url': 'https://bair.berkeley.edu/blog/',
            'source_type': 'RSS',
            'feed_url': 'https://bair.berkeley.edu/blog/feed.xml'
        },
        {
            'name': 'CMU Machine Learning Blog',
            'url': 'https://blog.ml.cmu.edu/',
            'source_type': 'RSS',
            'feed_url': 'https://blog.ml.cmu.edu/feed/'
        },
        {
            'name': 'AWS Machine Learning Blog',
            'url': 'https://aws.amazon.com/blogs/machine-learning/',
            'source_type': 'RSS',
            'feed_url': 'https://aws.amazon.com/blogs/machine-learning/feed/'
        },
        {
            'name': 'Google AI Blog',
            'url': 'https://blog.google/technology/ai/',
            'source_type': 'RSS',
            'feed_url': 'https://blog.google/technology/ai/rss/'
        },
        {
            'name': 'Towards Data Science',
            'url': 'https://towardsdatascience.com/',
            'source_type': 'RSS',
            'feed_url': 'https://towardsdatascience.com/feed'
        },
        {
            'name': 'Analytics Vidhya',
            'url': 'https://www.analyticsvidhya.com/blog/',
            'source_type': 'RSS',
            'feed_url': 'https://www.analyticsvidhya.com/blog/feed/'
        },
        {
            'name': 'MarkTechPost',
            'url': 'https://www.marktechpost.com/',
            'source_type': 'RSS',
            'feed_url': 'https://marktechpost.com/feed/'
        },
        {
            'name': 'Real Python',
            'url': 'https://realpython.com/',
            'source_type': 'RSS',
            'feed_url': 'https://realpython.com/atom.xml'
        },
        {
            'name': 'Planet Python',
            'url': 'https://planetpython.org/',
            'source_type': 'RSS',
            'feed_url': 'https://planetpython.org/rss20.xml'
        },
        {
            'name': 'Python Official Blog',
            'url': 'https://blog.python.org/',
            'source_type': 'RSS',
            'feed_url': 'https://blog.python.org/feeds/posts/default'
        },
        {
            'name': 'PyImageSearch',
            'url': 'https://pyimagesearch.com/blog/',
            'source_type': 'RSS',
            'feed_url': 'https://pyimagesearch.com/feed/'
        },
        {
            'name': 'CSS-Tricks',
            'url': 'https://css-tricks.com/',
            'source_type': 'RSS',
            'feed_url': 'https://css-tricks.com/feed/'
        },
        {
            'name': 'Smashing Magazine',
            'url': 'https://www.smashingmagazine.com/',
            'source_type': 'RSS',
            'feed_url': 'https://www.smashingmagazine.com/feed/'
        },
        {
            'name': 'A List Apart',
            'url': 'https://alistapart.com/',
            'source_type': 'RSS',
            'feed_url': 'https://alistapart.com/main/feed/'
        },
        {
            'name': 'Web.dev',
            'url': 'https://web.dev/blog/',
            'source_type': 'RSS',
            'feed_url': 'https://web.dev/feed.xml'
        },
        {
            'name': 'BetterExplained',
            'url': 'https://betterexplained.com/',
            'source_type': 'RSS',
            'feed_url': 'https://betterexplained.com/feed/'
        },
        {
            'name': 'MIT CSAIL News',
            'url': 'https://www.csail.mit.edu/news',
            'source_type': 'RSS',
            'feed_url': 'https://www.csail.mit.edu/news/rss.xml'
        },
        {
            'name': 'Apple Machine Learning Research',
            'url': 'https://machinelearning.apple.com/',
            'source_type': 'RSS',
            'feed_url': 'https://machinelearning.apple.com/rss.xml'
        },
        {
            'name': 'TensorFlow Blog',
            'url': 'https://blog.tensorflow.org/',
            'source_type': 'RSS',
            'feed_url': 'https://blog.tensorflow.org/feeds/posts/default'
        },
        {
            'name': 'PyTorch Blog',
            'url': 'https://pytorch.org/blog/',
            'source_type': 'RSS',
            'feed_url': 'https://pytorch.org/feed.xml'
        },
        {
            'name': 'KDnuggets',
            'url': 'https://www.kdnuggets.com/',
            'source_type': 'RSS',
            'feed_url': 'https://www.kdnuggets.com/feed'
        }
    ]
    
    for source_data in sources:
        existing = db.query(Source).filter(Source.name == source_data['name']).first()
        if not existing:
            source = Source(**source_data)
            db.add(source)
            logger.info(f"Added source: {source_data['name']}")
        else:
            logger.info(f"Source already exists: {source_data['name']}")
    
    db.commit()
    db.close()
    logger.info("Source seeding completed")


if __name__ == "__main__":
    seed_sources()

