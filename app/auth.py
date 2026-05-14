from datetime import datetime, timedelta
from passlib.context import CryptContext

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.database import get_db
from app import models
from sqlalchemy.orm import Session

from app.logger import logger


SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)

# =========================
# Password Hashing
# =========================
def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# =========================
# JWT Token
# =========================
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# =========================
# JWT Authentication & Role-Based Authorization
# =========================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid authentication"
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

        if user_id is None:

            # WARNING -> Invalid token payload
            logger.warning("Token validation failed: Missing user_id")

            raise credentials_exception

    except JWTError:

        # ERROR -> JWT decoding/validation failed
        logger.error("JWT token validation failed")

        raise credentials_exception

    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if user is None:

        # WARNING -> User from token does not exist
        logger.warning(f"Token user not found: {user_id}")

        raise credentials_exception

    # INFO -> Successful token validation
    logger.info(f"Token validated for user ID: {user.id}")

    return user


def admin_only(current_user=Depends(get_current_user)):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admins only"
        )

    return current_user