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
    from .common import Region, User_Notification
    from .product import Media, Shop, Comment, Product
    from .order import Order, Delivery_Process, Bucket, Promo_Code_Report
    from .payment import Payment_Process, Transaction_Log

class User(BaseMain):
    __tablename__ = "user"

    email:Mapped[str] = mapped_column(String(100), nullable=False, unique= True)
    first_name:Mapped[str] = mapped_column(String(50))
    age:Mapped[int] =mapped_column(SmallInteger)
    last_name:Mapped[str] = mapped_column(String(50))
    password:Mapped[str] = mapped_column(String(250), nullable=False)
    bio:Mapped[str] = mapped_column(Text,  nullable=True)
    tell_number:Mapped[int] = mapped_column(BigInteger, nullable=True)
    image_id:Mapped[int] = mapped_column(BigInteger, ForeignKey("media.id", ondelete="SET NULL"), nullable=True)
    password_hash:Mapped[str] = mapped_column(String(255), nullable=True)
    last_login:Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    garbage_email:Mapped[str] = mapped_column(String(100), default=None, nullable=True) # deleted email is => garbage_email
    is_active:Mapped[bool] = mapped_column(Boolean, default=True, )
    is_deleted:Mapped[bool] = mapped_column(Boolean, default=False, )
    is_staff:Mapped[bool] = mapped_column(Boolean, default=False, ) # First login is => staff bydefault
    is_admin:Mapped[bool] = mapped_column(Boolean, default=False, )
    is_courier:Mapped[bool] = mapped_column(Boolean, default=False,) 

    def __repr__(self):
        return f"user email: {self.email}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    media:Mapped[list["Media"]] = relationship("Media", back_populates="user", lazy="raise_on_sql")  #  USER 1:M IMAGE

    user_notification:Mapped[list["User_Notification"]] = relationship("User_Notification", back_populates="user", lazy = "raise_on_sql")
    order:Mapped["Order"] = relationship("Order", back_populates="user", lazy="raise_on_sql")
    bucket:Mapped["Bucket"] = relationship("Bucket", back_populates="user", lazy="raise_on_sql")
    promo_code_report:Mapped[list["Promo_Code_Report"]] = relationship("Promo_Code_Report", back_populates="user", lazy="raise_on_sql")
    payment_process:Mapped[list["Payment_Process"]]  = relationship("Payment_Process", back_populates="user", lazy="raise_on_sql")
    shop:Mapped[Shop] = relationship("Shop", back_populates="user", lazy="raise_on_sql")                            # User 1:1 Shop
    comment:Mapped[list["Comment"]] = relationship("Comment", back_populates="user", lazy="raise_on_sql")
    user_address:Mapped[list["User_Address"]] = relationship("User_Address", back_populates="user", lazy="raise_on_sql")
    courier_profile:Mapped["Courier_Profile"] = relationship("Courier_Profile", back_populates="user", lazy="raise_on_sql")   # USER 1:1 COURIER_PROFILE 
    wallet:Mapped["Wallet"] = relationship("Wallet", back_populates="user", lazy="raise_on_sql")
    like:Mapped[list["Like"]] = relationship("Like", back_populates="user", lazy="raise_on_sql")

class User_Address(BaseMain):
    __tablename__ = "user_address"

    user_id:Mapped[int] = mapped_column(SmallInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    region_id:Mapped[int] = mapped_column(SmallInteger, ForeignKey("region.id", ondelete="SET NULL"), nullable=False)
    address:Mapped[str] = mapped_column(String(250), nullable=False)


    def __repr__(self):
        return f"user address: {self.address}"

    user:Mapped["User"] = relationship("User", back_populates="user_address", lazy="raise_on_sql")
    region:Mapped["Region"] = relationship("Region", back_populates="user_address", lazy="raise_on_sql")

    order:Mapped[list["Order"]] = relationship("Order", back_populates="user_address", lazy="raise_on_sql")
    delivery_process:Mapped[list["Delivery_Process"]] = relationship("Delivery_Process", back_populates="user_address", lazy="raise_on_sql")

class Courier_Profile(BaseMain):
    __tablename__ = "courier_profile"

    user_id:Mapped[int] = mapped_column(SmallInteger, ForeignKey("user.id", ondelete = "CASCADE"), unique=True, nullable=False)
    transport_type:Mapped[str] = mapped_column(String(200), default=None)
    unique_number:Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    is_ready:Mapped[bool] = mapped_column(Boolean, nullable=True)
    balance:Mapped[float] = mapped_column(Float, default=None)

    def __repr__(self):
        return f"Courier id: {self.user_id}"

    user:Mapped["User"] = relationship("User", back_populates="courier_profile", lazy="raise_on_sql")

    delivery_process:Mapped[list["Delivery_Process"]] = relationship("Delivery_Process", back_populates="courier_profile", lazy="raise_on_sql")

class Wallet(BaseMain):
    __tablename__ = "wallet"

    user_id:Mapped[int] = mapped_column(SmallInteger, ForeignKey("user.id", ondelete="CASCADE"), unique=True, nullable=False)
    balance:Mapped[float] = mapped_column(Float, default=None)
    currency:Mapped[str] = mapped_column(String(10), default="USD")
    is_blocked:Mapped[bool] = mapped_column(Boolean, default=False)
 

    def __repr__(self):
        return f"Wallet id: {self.user_id}"

    user:Mapped["User"] = relationship("User", back_populates="wallet", lazy="raise_on_sql")
    payment_process:Mapped[list["Payment_Process"]] = relationship("Payment_Process", back_populates="wallet", lazy="raise_on_sql")
    transaction_log:Mapped[list["Transaction_Log"]] = relationship("Transaction_Log", back_populates="wallet", lazy="raise_on_sql")

class Like(BaseMain):
    __tablename__ = "like"
    user_id:Mapped[int] = mapped_column(SmallInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    product_id:Mapped[int] = mapped_column(SmallInteger, ForeignKey("product.id", ondelete="CASCADE"), nullable=False)

    user:Mapped["User"] = relationship("User", back_populates="like", lazy="raise_on_sql")
    product:Mapped["Product"] = relationship("Product", back_populates="like", lazy="raise_on_sql")