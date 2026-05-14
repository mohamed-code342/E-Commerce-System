from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.logger import logger

DATABASE_URL = "sqlite:///./ecommerce.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# =========================
# Simulated Database Failure
# Test database connection on startup
# Log critical error if connection fails
# =========================

try:
    engine.connect()

except Exception as e:

    # CRITICAL -> Critical system failures
    logger.critical(f"Database connection failed: {str(e)}")
# Create database session factory - when API needs db
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all database models
Base = declarative_base()

# Dependency to get database session
# Automatically closes session after request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()