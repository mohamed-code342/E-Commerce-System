from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


# =========================
# Add To Cart
# =========================

@router.post("/", response_model=schemas.CartResponse)
def add_to_cart(
    cart: schemas.CartCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    product = db.query(models.Product).filter(
        models.Product.id == cart.product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing_item = db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id,
        models.CartItem.product_id == cart.product_id
    ).first()

    current_quantity = existing_item.quantity if existing_item else 0
    new_quantity = current_quantity + cart.quantity

    if new_quantity > product.stock:
        raise HTTPException(
            status_code=400,
            detail=f"Only {product.stock} items available in stock"
        )

    if existing_item:
        existing_item.quantity = new_quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item

    cart_item = models.CartItem(
        user_id=current_user.id,
        product_id=cart.product_id,
        quantity=cart.quantity
    )

    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return cart_item

# =========================
# Get User Cart
# =========================

@router.get("/", response_model=list[schemas.CartResponse])
def get_cart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id
    ).all()


# =========================
# Remove Cart Item
# =========================

@router.delete("/{cart_item_id}")
def remove_cart_item(
    cart_item_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    cart_item = db.query(models.CartItem).filter(
        models.CartItem.id == cart_item_id,
        models.CartItem.user_id == current_user.id
    ).first()

    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    db.delete(cart_item)
    db.commit()

    return {
        "message": "Item removed from cart"
    }


# =========================
# Endpoint for editing amout/total price after qty is 2 or more
# =========================

@router.put("/{cart_item_id}", response_model=schemas.CartResponse)
def update_cart_item(
    cart_item_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.id == cart_item_id,
        models.CartItem.user_id == current_user.id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    product = db.query(models.Product).filter(
        models.Product.id == cart_item.product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if quantity <= 0:
        db.delete(cart_item)
        db.commit()
        return cart_item

    if quantity > product.stock:
        raise HTTPException(
            status_code=400,
            detail=f"Only {product.stock} items available in stock"
        )

    cart_item.quantity = quantity

    db.commit()
    db.refresh(cart_item)

    return cart_item