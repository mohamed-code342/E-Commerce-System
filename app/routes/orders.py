from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.auth import get_current_user, admin_only
from app.logger import logger

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


# =========================
# Create Order From Cart With Stock Validation
# =========================

@router.post("/", response_model=schemas.OrderResponse)
def create_order(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # DEBUG -> Detailed debugging information
    logger.debug(f"Current user ID: {current_user.id}")

    cart_items = db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id
    ).all()

    if not cart_items:

        logger.error("Cart is empty during checkout") # ERROR -> Application errors

        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )

    total_price = 0

    for item in cart_items:
        product = db.query(models.Product).filter(
            models.Product.id == item.product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for product: {product.name}"
            )

        total_price += product.price * item.quantity

    new_order = models.Order(
        user_id=current_user.id,
        total_price=total_price
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in cart_items:
        product = db.query(models.Product).filter(
            models.Product.id == item.product_id
        ).first()

        order_item = models.OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )

        product.stock -= item.quantity
        db.add(order_item)

    db.commit()

    for item in cart_items:
        db.delete(item)

    db.commit()

    return new_order


# =========================
# Get User Orders
# =========================

@router.get("/", response_model=list[schemas.OrderResponse])
def get_orders(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return db.query(models.Order).filter(
        models.Order.user_id == current_user.id
    ).all()


# =========================
# Admin Get All Orders
# =========================

@router.get("/all", response_model=list[schemas.OrderResponse])
def get_all_orders(
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):

    return db.query(models.Order).all()