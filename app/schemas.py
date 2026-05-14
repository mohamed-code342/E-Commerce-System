from pydantic import BaseModel, EmailStr

# Request validation using Pydantic models - Schemas to manage everything
# Use of response models for consistent output formatting

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category_id: int


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int
    category_id: int

    class Config:
        from_attributes = True    


# =========================
# Category Schemas
# =========================

class CategoryCreate(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# =========================
# Cart Schemas
# =========================

class CartCreate(BaseModel):
    product_id: int
    quantity: int


class CartResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True

# =========================
# Order Schemas
# =========================

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float

    class Config:
        from_attributes = True