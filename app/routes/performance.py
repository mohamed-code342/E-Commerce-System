import time

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.cache import get_cache, set_cache


router = APIRouter(
    prefix="/performance",
    tags=["Performance"]
)


# =========================
# Cache Performance Test
# =========================

@router.get("/cache-test")
def cache_performance_test(db: Session = Depends(get_db)):

    cache_key = "performance_products_test"

    # Measure database response time
    db_start = time.time()

    products = db.query(models.Product).all()

    db_time = time.time() - db_start

    product_data = [
        {
            "id": product.id,
            "name": product.name,
            "price": product.price
        }
        for product in products
    ]

    set_cache(cache_key, product_data, expire=120)

    # Measure cache response time
    cache_start = time.time()

    cached_products = get_cache(cache_key)

    cache_time = time.time() - cache_start

    improvement = 0

    if db_time > 0:
        improvement = ((db_time - cache_time) / db_time) * 100

    return {
        "database_response_time_seconds": round(db_time, 6),
        "cache_response_time_seconds": round(cache_time, 6),
        "performance_improvement_percent": round(improvement, 2),
        "total_products_tested": len(cached_products) if cached_products else 0
    }