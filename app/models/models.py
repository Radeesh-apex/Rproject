from sqlalchemy import Column, BigInteger, String, Text, DECIMAL, Integer, ForeignKey, Enum, TIMESTAMP, text, Index
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship, DeclarativeBase
import enum

class Base(DeclarativeBase):
    pass

# --- Enums matching your SQL ---
class UserRole(enum.Enum):
    customer = "customer"
    seller = "seller"
    admin = "admin"

class OrderStatus(enum.Enum):
    pending = "pending"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

# --- Models ---

class User(Base):
    __tablename__ = "users"
    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), unique=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    phone = Column(String(20))
    role = Column(Enum(UserRole), server_default="customer")
    addresses = Column(JSON)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    # Relationships
    products = relationship("Product", back_populates="seller")
    orders = relationship("Order", back_populates="user")

class Product(Base):
    __tablename__ = "products"
    product_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(500), nullable=False)
    description = Column(Text)
    sku = Column(String(100), unique=True, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    stock_quantity = Column(Integer, server_default="0")
    seller_id = Column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    category_id = Column(BigInteger, ForeignKey("categories.category_id", ondelete="SET NULL"))
    brand_id = Column(BigInteger, ForeignKey("brands.brand_id", ondelete="SET NULL"))
    images = Column(JSON)
    metadata_json = Column("metadata", JSON) # 'metadata' is reserved in SQLAlchemy, so we rename the attribute
    
    seller = relationship("User", back_populates="products")

class Category(Base):
    __tablename__ = "categories"
    category_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    parent_id = Column(BigInteger, ForeignKey("categories.category_id", ondelete="SET NULL"))

class Order(Base):
    __tablename__ = "orders"
    order_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum(OrderStatus), server_default="pending")
    shipping_address = Column(JSON, nullable=False)
    
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    order_item_id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_id = Column(BigInteger, ForeignKey("orders.order_id", ondelete="CASCADE"), nullable=False)
    product_id = Column(BigInteger, ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")