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
# =========================

try:
    engine.connect()

except Exception as e:

    # CRITICAL -> Critical system failures
    logger.critical(f"Database connection failed: {str(e)}")


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()