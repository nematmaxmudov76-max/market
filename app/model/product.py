from __future__ import annotations

from datetime import datetime
from unittest.mock import Base
from sqlalchemy import (
    String,
    BigInteger,
    Boolean,
    Text,
    SmallInteger,
    Float,
    DECIMAL,
    DateTime,
    ForeignKey,
    func,
)
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.model.base import BaseMain

if TYPE_CHECKING:
    from .order import Order_Item, Bucket_Product
    from .user import User, Like


class  Shop(BaseMain):
    __tablename__ = "shop"

    name:Mapped[str] = mapped_column(String(150), nullable=False)
    user_id:Mapped[int] = mapped_column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), unique=True, nullable=False)
    # banner_id:Mapped[int] = mapped_column(BigInteger, ForeignKey("media.id", ondelete = "CASCADE"), nullable=False)
    image_id:Mapped[int] = mapped_column(BigInteger, ForeignKey("media.id", ondelete = "CASCADE") )
    description:Mapped[str] = mapped_column(Text, default=None)
    rating:Mapped[int] = mapped_column(BigInteger, default=None)
    is_active:Mapped[bool] = mapped_column(Boolean, default=None)

    def __repr__(self):
        return f"shop name: {self.name}"
    user:Mapped["User"] = relationship("User", back_populates="shop", lazy="raise_on_sql")
    media:Mapped[list["Media"]] = relationship("Media", back_populates="shop",  lazy="raise_on_sql")
    shop_product:Mapped[list["Shop_Product"]] = relationship("Shop_Product", back_populates="shop", lazy="raise_on_sql")

    # shop_banner:Mapped[list["Media"]] = relationship("Media", back_populates="media_banner", foreign_keys=[banner_id], lazy="raise_on_sql")
        


class Media(BaseMain):
    __tablename__ = "media"

    file_url:Mapped[str] = mapped_column(String(255))

    def __repr__(self):
        return f"file url: {self.file_url}"

    # media_banner:Mapped["Shop"] = relationship("Shop", back_populates="shop_banner", foreign_keys="Shop.banner_id", lazy="raise_on_sql")
    shop:Mapped["Shop"] = relationship("Shop", back_populates="media",  lazy="raise_on_sql")
    product_media:Mapped[list["Product_Media"]] = relationship("Product_Media", back_populates="media", lazy="raise_on_sql")
    user:Mapped["User"] = relationship("User", back_populates="media", lazy="raise_on_sql")


class Product(BaseMain):
    __tablename__ = "product"

    name:Mapped[str] = mapped_column(String(150))
    description:Mapped[str] = mapped_column(Text)
    price:Mapped[float] = mapped_column(Float, default=None)
    current_quantity:Mapped[int] = mapped_column(BigInteger, default=None)
    expiration_date:Mapped[datetime] = mapped_column(DateTime(timezone=True))
    size:Mapped[float] = mapped_column(Float, default=None)
    rating:Mapped[int] = mapped_column(SmallInteger, default=None)
    liked_count:Mapped[int] = mapped_column(BigInteger, default=None)
    is_active:Mapped[bool] = mapped_column(Boolean, default=None)

    def __repr__(self):
        return f"product name:{self.name}"
    order_item:Mapped[list["Order_Item"]] = relationship("Order_Item", back_populates = "product", lazy="raise_on_sql")
    bucket_product:Mapped[list["Bucket_Product"]] = relationship("Bucket_Product", back_populates="product", lazy="raise_on_sql")
    product_media:Mapped[list["Product_Media"]] = relationship("Product_Media", back_populates="product", lazy="raise_on_sql")
    product_category:Mapped[list["Product_Category"]] = relationship("Product_Category", back_populates="product", lazy="raise_on_sql")
    comment:Mapped[list["Comment"]] = relationship("Comment", back_populates="product", lazy="raise_on_sql")
    shop_product:Mapped[list["Shop_Product"]] = relationship("Shop_Product", back_populates="product", lazy="raise_on_sql")
    like:Mapped[list["Like"]] = relationship("Like", back_populates="product", lazy="raise_on_sql")

class Category(BaseMain):
    __tablename__ = "category"

    name:Mapped[str] = mapped_column(String(80), nullable=False)

    def __repr__(self):
        return f"category : {self.name}"

    product_category:Mapped[list["Product_Category"]] = relationship("Product_Category", back_populates="category", lazy="raise_on_sql")

class Product_Media(BaseMain):
    __tablename__ = "product_media"

    product_id:Mapped[int] = mapped_column(SmallInteger, ForeignKey("product.id", ondelete="SET NULL"), nullable=False)
    media_id:Mapped[int] = mapped_column(SmallInteger, ForeignKey("media.id", ondelete="SET NULL"), nullable=False)

    def __repr__(self):
        return f"product id:{self.product_id}, media id:{self.media_id}"

    product:Mapped["Product"] = relationship("Product", back_populates="product_media", lazy="raise_on_sql")
    media:Mapped["Media"] = relationship("Media", back_populates="product_media", lazy="raise_on_sql")


class Product_Category(BaseMain):
    __tablename__="product_category"

    product_id:Mapped[int] = mapped_column(SmallInteger, ForeignKey("product.id", ondelete="SET NULL"), nullable=False)
    category_id:Mapped[int] = mapped_column(SmallInteger, ForeignKey("category.id", ondelete="SET NULL"), onupdate=False)

    def __repr__(self):
        return f"product id:{self.product_id}, category id:{self.category_id}"

    product:Mapped["Product"] = relationship("Product", back_populates="product_category", lazy="raise_on_sql")
    category:Mapped["Category"] = relationship("Category", back_populates="product_category", lazy="raise_on_sql")


class Shop_Product(BaseMain):
    __tablename__ ="shop_product"

    shop_id:Mapped[int] = mapped_column(SmallInteger, ForeignKey("shop.id", ondelete="SET NULL"), nullable=False)
    product_id:Mapped[int] = mapped_column(SmallInteger, ForeignKey("product.id", ondelete="SET NULL"), nullable=False)

    def __repr__(self):
        return f"shop id:{self.shop_id}, product id:{self.product_id}"

    shop:Mapped["Shop"] = relationship("Shop", back_populates="shop_product", lazy="raise_on_sql")
    product:Mapped["Product"] = relationship("Product", back_populates="shop_product", lazy="raise_on_sql")




class Comment(BaseMain):
    __tablename__ = "comment"

    user_id:Mapped[int] = mapped_column(SmallInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    product_id:Mapped[int] = mapped_column(SmallInteger, ForeignKey("product.id", ondelete="CASCADE"), nullable=False)
    title:Mapped[str] = mapped_column(Text, nullable=False)
    is_active:Mapped[bool] = mapped_column(Boolean, default=True)
    deleted_comment:Mapped[str] = mapped_column(Text, default=None) # deleted comment is => deleted_comment

    def __repr__(self):
        return f"user id:{self.user_id}, product id:{self.product_id}, title:{self.title}"

    user:Mapped["User"] = relationship("User", back_populates="comment", lazy="raise_on_sql")
    product:Mapped["Product"] = relationship("Product", back_populates="comment", lazy="raise_on_sql")













