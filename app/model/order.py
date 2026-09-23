from __future__ import annotations

from datetime import datetime
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
    from .product import Product
    from .user import User_Address, User, Courier_Profile
    from .payment import Payment_Process


class Order(BaseMain):
    __tablename__ = "order"

    user_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("user.id", ondelete="SET NULL"), nullable=False
    )
    total_amount: Mapped[float] = mapped_column(Float, default=None)
    order_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    address_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("user_address.id", ondelete="SET NULL"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(100), default="pending")

    def __repr__(self):
        return f"user id: {self.user_id}, total amount: {self.total_amount}, status: {self.status}, order number: {self.order_number}, address id: {self.address_id}"

    user: Mapped["User"] = relationship(
        "User", back_populates="order", lazy="raise_on_sql"
    )
    user_address: Mapped["User_Address"] = relationship(
        "User_Address", back_populates="order", lazy="raise_on_sql"
    )
    delivery_process: Mapped["Delivery_Process"] = relationship(
        "Delivery_Process", back_populates="order", lazy="raise_on_sql"
    )
    order_item: Mapped[list["Order_Item"]] = relationship(
        "Order_Item", back_populates="order", lazy="raise_on_sql"
    )
    promo_code_report: Mapped[list["Promo_Code_Report"]] = relationship(
        "Promo_Code_Report", back_populates="order", lazy="raise_on_sql"
    )
    payment_process: Mapped[list["Payment_Process"]] = relationship(
        "Payment_Process", back_populates="order", lazy="raise_on_sql"
    )


class Delivery_Process(BaseMain):
    __tablename__ = "delivery_process"

    courier_id: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey("courier_profile.id", ondelete="SET NULL"),
        nullable=False,
    )
    order_id: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey("order.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    address_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("user_address.id", ondelete="SET NULL"), nullable=False
    )
    delivery_fee: Mapped[float] = mapped_column(Float, default=None)
    status: Mapped[str] = mapped_column(String(100), default="pending")
    tracking_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    taken_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=None)
    delivered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=None
    )

    def __repr__(self):
        return f"courier id: {self.courier_id}, order id: {self.order_id}, address id: {self.address_id}, status: {self.status}"

    courier_profile: Mapped["Courier_Profile"] = relationship(
        "Courier_Profile", back_populates="delivery_process", lazy="raise_on_sql"
    )
    order: Mapped["Order"] = relationship(
        "Order", back_populates="delivery_process", lazy="raise_on_sql"
    )
    user_address: Mapped["User_Address"] = relationship(
        "User_Address", back_populates="delivery_process", lazy="raise_on_sql"
    )


class Order_Item(BaseMain):
    __tablename__ = "order_item"

    order_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("order.id", ondelete="SET NULL"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("product.id", ondelete="SET NULL"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(BigInteger, default=None)

    def __repr__(self):
        return f"order id: {self.order_id}, product id: {self.product_id}, quantity: {self.quantity}"

    order: Mapped["Order"] = relationship(
        "Order", back_populates="order_item", lazy="raise_on_sql"
    )
    product: Mapped["Product"] = relationship(
        "Product", back_populates="order_item", lazy="raise_on_sql"
    )


class Bucket(BaseMain):
    __tablename__ = "bucket"

    user_id: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey("user.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self):
        return f"user id: {self.user_id}, is active: {self.is_active}"

    user: Mapped["User"] = relationship(
        "User", back_populates="bucket", lazy="raise_on_sql"
    )
    bucket_product: Mapped[list["Bucket_Product"]] = relationship(
        "Bucket_Product", back_populates="bucket", lazy="raise_on_sql"
    )


class Bucket_Product(BaseMain):
    __tablename__ = "bucket_product"

    bucket_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("bucket.id", ondelete="SET NULL"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("product.id", ondelete="SET NULL"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(BigInteger, default=None)
    total_price: Mapped[float] = mapped_column(Float, default=None)
    is_checked:Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f"bucket id: {self.bucket_id}, product id: {self.product_id}, quantity: {self.quantity}, total price: {self.total_price}"

    bucket: Mapped["Bucket"] = relationship(
        "Bucket", back_populates="bucket_product", lazy="raise_on_sql"
    )
    product: Mapped["Product"] = relationship(
        "Product", back_populates="bucket_product", lazy="raise_on_sql"
    )


class Promo_Code(BaseMain):
    __tablename__ = "promo_code"

    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    discount_percentage: Mapped[float] = mapped_column(Float, default=None)
    discount_amount: Mapped[float] = mapped_column(Float, default=None)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self):
        return f"promo code: {self.code}, discount percentage: {self.discount_percentage}, discount amount: {self.discount_amount}, is active: {self.is_active}"

    promo_code_report: Mapped[list["Promo_Code_Report"]] = relationship(
        "Promo_Code_Report", back_populates="promo_code", lazy="raise_on_sql"
    )


class Promo_Code_Report(BaseMain):
    __tablename__ = "promo_code_report"

    promo_code_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("promo_code.id", ondelete="SET NULL"), nullable=False
    )
    order_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("order.id", ondelete="SET NULL"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("user.id", ondelete="SET NULL"), nullable=False
    )
    used_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=None)

    def __repr__(self):
        return f"promo code used at: {self.used_at}"

    promo_code: Mapped["Promo_Code"] = relationship(
        "Promo_Code", back_populates="promo_code_report", lazy="raise_on_sql"
    )
    order: Mapped["Order"] = relationship(
        "Order", back_populates="promo_code_report", lazy="raise_on_sql"
    )
    user: Mapped["User"] = relationship(
        "User", back_populates="promo_code_report", lazy="raise_on_sql"
    )
