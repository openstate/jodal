from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings
import logging

logger = logging.getLogger(__name__)

# Configure the connection pool
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=10,  # Increase from default of 5
    max_overflow=20,  # Increase from default of 10
    pool_timeout=60,  # Increase timeout
    pool_pre_ping=True,  # Enable connection health checks
    pool_recycle=28000  # Recycle connections after 1 hour
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    # Import all models explicitly to ensure they're registered with SQLAlchemy
    from .models import (
        Session,
        SessionFeedback,
        Message,
        Document,
        MessageFeedback,
        DocumentFeedback,
        MessageDocument
        
    )
    
    def table_exists(table_name):
        try:
            with engine.connect() as conn:
                return engine.dialect.has_table(conn, table_name)
        except Exception:
            return False
    
    try:
        # Create all tables that don't exist
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized")
        
        # Log which tables exist for debugging
        existing_tables = [name for name in Base.metadata.tables.keys()]
        logger.info(f"Existing tables: {existing_tables}")
        
    except Exception as e:
        logger.error(f"Error during database initialization: {str(e)}", exc_info=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        try:
            db.rollback()
        except Exception:
            pass  # Ignore rollback errors
        raise
    finally:
        try:
            db.close()
        except Exception:
            pass  # Ignore close errors

