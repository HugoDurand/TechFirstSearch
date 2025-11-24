import logging
from database import init_db
from seed_sources import seed_sources

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_railway_db():
    logger.info("Initializing database...")
    init_db()
    logger.info("Database tables created")
    
    logger.info("Seeding sources...")
    seed_sources()
    logger.info("Sources seeded successfully")
    
    logger.info("Railway database initialization complete!")

if __name__ == "__main__":
    initialize_railway_db()

