from typing import List

from sqlalchemy import BigInteger, Column, DECIMAL, ForeignKeyConstraint, Index, Integer, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import ENUM, TIMESTAMP, TINYINT
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class Categories(Base):
    __tablename__ = 'categories'
    __table_args__ = (
        Index('idx_category_name', 'name'),
    )

    id = mapped_column(BigInteger, primary_key=True)
    name = mapped_column(String(100, 'utf8mb4_unicode_ci'), nullable=False)
    description = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    created_at = mapped_column(TIMESTAMP(fsp=6), server_default=text('CURRENT_TIMESTAMP(6)'))
    updated_at = mapped_column(TIMESTAMP(fsp=6), server_default=text('CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)'))

    products: Mapped[List['Products']] = relationship('Products', uselist=True, back_populates='category')


class Customers(Base):
    __tablename__ = 'customers'
    __table_args__ = (
        Index('email', 'email', unique=True),
        Index('idx_customer_email', 'email'),
        Index('idx_customer_name', 'last_name', 'first_name')
    )

    id = mapped_column(BigInteger, primary_key=True)
    first_name = mapped_column(String(50, 'utf8mb4_unicode_ci'), nullable=False)
    last_name = mapped_column(String(50, 'utf8mb4_unicode_ci'), nullable=False)
    email = mapped_column(String(100, 'utf8mb4_unicode_ci'), nullable=False)
    phone = mapped_column(String(20, 'utf8mb4_unicode_ci'))
    address = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    created_at = mapped_column(TIMESTAMP(fsp=6), server_default=text('CURRENT_TIMESTAMP(6)'))
    updated_at = mapped_column(TIMESTAMP(fsp=6), server_default=text('CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)'))

    orders: Mapped[List['Orders']] = relationship('Orders', uselist=True, back_populates='customer')


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        Index('email', 'email', unique=True),
        Index('idx_email', 'email'),
        Index('idx_username', 'username'),
        Index('username', 'username', unique=True)
    )

    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(50), nullable=False)
    email = mapped_column(String(100), nullable=False)
    created_at = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    posts: Mapped[List['Posts']] = relationship('Posts', uselist=True, back_populates='user')


class Orders(Base):
    __tablename__ = 'orders'
    __table_args__ = (
        ForeignKeyConstraint(['customer_id'], ['customers.id'], ondelete='CASCADE', name='orders_ibfk_1'),
        Index('idx_customer_id', 'customer_id'),
        Index('idx_order_date', 'order_date'),
        Index('idx_status', 'status')
    )

    id = mapped_column(BigInteger, primary_key=True)
    customer_id = mapped_column(BigInteger, nullable=False)
    total_amount = mapped_column(DECIMAL(10, 2), nullable=False, server_default=text("'0.00'"))
    order_date = mapped_column(TIMESTAMP(fsp=6), server_default=text('CURRENT_TIMESTAMP(6)'))
    status = mapped_column(ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled'), server_default=text("'pending'"))
    shipping_address = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    created_at = mapped_column(TIMESTAMP(fsp=6), server_default=text('CURRENT_TIMESTAMP(6)'))
    updated_at = mapped_column(TIMESTAMP(fsp=6), server_default=text('CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)'))

    customer: Mapped['Customers'] = relationship('Customers', back_populates='orders')
    order_items: Mapped[List['OrderItems']] = relationship('OrderItems', uselist=True, back_populates='order')


class Posts(Base):
    __tablename__ = 'posts'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], name='posts_ibfk_1'),
        Index('idx_created_at', 'created_at'),
        Index('idx_user_id', 'user_id')
    )

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, nullable=False)
    title = mapped_column(String(200), nullable=False)
    content = mapped_column(Text)
    created_at = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    user: Mapped['Users'] = relationship('Users', back_populates='posts')


class Products(Base):
    __tablename__ = 'products'
    __table_args__ = (
        ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='CASCADE', name='products_ibfk_1'),
        Index('idx_category_id', 'category_id'),
        Index('idx_price', 'price'),
        Index('idx_product_name', 'name')
    )

    id = mapped_column(BigInteger, primary_key=True)
    category_id = mapped_column(BigInteger, nullable=False)
    name = mapped_column(String(200, 'utf8mb4_unicode_ci'), nullable=False)
    price = mapped_column(DECIMAL(10, 2), nullable=False)
    stock_quantity = mapped_column(Integer, nullable=False, server_default=text("'0'"))
    description = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    is_active = mapped_column(TINYINT(1), server_default=text("'1'"))
    created_at = mapped_column(TIMESTAMP(fsp=6), server_default=text('CURRENT_TIMESTAMP(6)'))
    updated_at = mapped_column(TIMESTAMP(fsp=6), server_default=text('CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)'))

    category: Mapped['Categories'] = relationship('Categories', back_populates='products')
    order_items: Mapped[List['OrderItems']] = relationship('OrderItems', uselist=True, back_populates='product')


class OrderItems(Base):
    __tablename__ = 'order_items'
    __table_args__ = (
        ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE', name='order_items_ibfk_1'),
        ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE', name='order_items_ibfk_2'),
        Index('idx_order_id', 'order_id'),
        Index('idx_product_id', 'product_id')
    )

    id = mapped_column(BigInteger, primary_key=True)
    order_id = mapped_column(BigInteger, nullable=False)
    product_id = mapped_column(BigInteger, nullable=False)
    quantity = mapped_column(Integer, nullable=False)
    unit_price = mapped_column(DECIMAL(10, 2), nullable=False)
    total_price = mapped_column(DECIMAL(10, 2), nullable=False)
    created_at = mapped_column(TIMESTAMP(fsp=6), server_default=text('CURRENT_TIMESTAMP(6)'))
    updated_at = mapped_column(TIMESTAMP(fsp=6), server_default=text('CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)'))

    order: Mapped['Orders'] = relationship('Orders', back_populates='order_items')
    product: Mapped['Products'] = relationship('Products', back_populates='order_items')
