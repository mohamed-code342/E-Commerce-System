from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


# =========================
# User Table
# =========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

    role = Column(String, default="customer")

    orders = relationship("Order", back_populates="user")


# =========================
# Category Table
# =========================
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    products = relationship("Product", back_populates="category")


# =========================
# Product Table
# =========================
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)

    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")


# =========================
# Order Table
# =========================

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    total_price = Column(Float, default=0)

    user = relationship("User", back_populates="orders")


# =========================
# Cart Table
# =========================

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    quantity = Column(Integer, default=1)


# =========================
# Order Items Table
# =========================

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    quantity = Column(Integer)


