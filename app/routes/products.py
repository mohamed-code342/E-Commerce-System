from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app import models, schemas
from app.auth import admin_only
from app.logger import logger

from app.cache import (
    get_cache,
    set_cache,
    delete_cache,
    clear_product_cache
)


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# =========================
# Create Product (Admin Only)
# =========================

@router.post("/", response_model=schemas.ProductResponse, status_code=201)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    new_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category_id=product.category_id
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    # Clear product cache after creating new product
    clear_product_cache()

    # INFO -> Product created successfully
    logger.info(f"Product created: {new_product.name}")

    return new_product


# =========================
# Get All Products With Cache Redis
# =========================

@router.get("/", response_model=list[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):

    cached_products = get_cache("products_all")

    if cached_products:

        # INFO -> Products loaded from cache
        logger.info("Products retrieved from Redis cache")

        return cached_products

    # DEBUG -> Fetching products from database
    logger.debug("Fetching all products from database")

    products = db.query(models.Product).all()

    product_data = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "category_id": product.category_id
        }
        for product in products
    ]

    set_cache("products_all", product_data)

    # INFO -> Products cached successfully
    logger.info("Products cached in Redis")

    return product_data

# =========================
# Search, Filter & Pagination Products
# =========================

@router.get("/search/", response_model=list[schemas.ProductResponse])
def search_products(
    name: Optional[str] = None,
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(models.Product)

    if name:
        query = query.filter(
            models.Product.name.ilike(f"%{name}%")
        )

    if category_id:
        query = query.filter(
            models.Product.category_id == category_id
        )

    if min_price is not None:
        query = query.filter(
            models.Product.price >= min_price
        )

    if max_price is not None:
        query = query.filter(
            models.Product.price <= max_price
        )

    offset = (page - 1) * limit

    # INFO -> Product search/filter executed
    logger.info(
        f"Product search executed | "
        f"name={name}, category_id={category_id}, "
        f"min_price={min_price}, max_price={max_price}, "
        f"page={page}, limit={limit}"
    )

    return query.offset(offset).limit(limit).all()


# =========================
# Get Product By ID With Cache
# =========================

@router.get("/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):

    cache_key = f"products_{product_id}"

    cached_product = get_cache(cache_key)

    if cached_product:

        # INFO -> Product loaded from cache
        logger.info(f"Product {product_id} retrieved from Redis cache")

        return cached_product

    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:

        # WARNING -> Product not found
        logger.warning(f"Product not found with ID: {product_id}")

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product_data = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock,
        "category_id": product.category_id
    }

    set_cache(cache_key, product_data)

    # INFO -> Product cached successfully
    logger.info(f"Product {product_id} cached in Redis")

    return product_data


# =========================
# Update Product (Admin Only)
# =========================

@router.put("/{product_id}", response_model=schemas.ProductResponse)
def update_product(
    product_id: int,
    updated_product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:

        # WARNING -> Product update failed
        logger.warning(f"Update failed. Product not found with ID: {product_id}")

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.name = updated_product.name
    product.description = updated_product.description
    product.price = updated_product.price
    product.stock = updated_product.stock
    product.category_id = updated_product.category_id

    db.commit()
    db.refresh(product)

    # Clear product cache after updating product
    clear_product_cache()

    # INFO -> Product updated successfully
    logger.info(f"Product updated: {product.name}")

    return product


# =========================
# Delete Product (Admin Only)
# =========================

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:

        # WARNING -> Product delete failed
        logger.warning(f"Delete failed. Product not found with ID: {product_id}")

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product_name = product.name

    db.delete(product)
    db.commit()

    # Clear product cache after deleting product
    clear_product_cache()

    # WARNING -> Product deleted
    logger.warning(f"Product deleted: {product_name}")

    return {
        "message": "Product deleted successfully"
    }