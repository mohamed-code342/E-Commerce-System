from fastapi import APIRouter, Depends, HTTPException
from app.auth import hash_password
from app.auth import verify_password, create_access_token
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.logger import logger

from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# ADMIN DETAILS: "id:3" "admin", "admin@gmail.com", "123456"

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
        role="customer"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    logger.info(f"User registered successfully: {user.email}") 

    return new_user


# =========================
# User Login
# =========================

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if not db_user:

        # WARNING -> Failed authentication attempt
        logger.warning(f"Failed login attempt: {user.email}")

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(user.password, db_user.password):

        # WARNING -> Incorrect password attempt
        logger.warning(f"Wrong password attempt: {user.email}")

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        data={
            "user_id": db_user.id,
            "role": db_user.role
        }
    )

    # INFO -> Successful login operation
    logger.info(f"User logged in successfully: {db_user.email}")

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# =========================
# Swagger Login for JWT Authorization
# =========================

@router.post("/token")
def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(
        models.User.email == form_data.username
    ).first()

    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        data={
            "user_id": db_user.id,
            "role": db_user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }