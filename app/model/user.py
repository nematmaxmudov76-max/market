from __future__ import annotations
from datetime import datetime
from sqlalchemy import (
    String,
    BigInteger,
    Boolean,
    Text,
    JSON,
    Integer,
    SmallInteger,
    Float,
    # DECIMAL,
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

    email: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    age: Mapped[int] = mapped_column(SmallInteger, nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    password_hash: Mapped[str] = mapped_column(String(250), nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    tell_number: Mapped[int] = mapped_column(BigInteger, nullable=True)
    image_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("media.id", ondelete="SET NULL"), nullable=True
    )
    last_login: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    garbage_email: Mapped[str] = mapped_column(
        String(100), default=None, nullable=True
    )  # deleted email is => garbage_email
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    is_merchant: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )  # first login is => is_admin = true
    is_manager: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    is_courier: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    def __repr__(self):
        return f"user email: {self.email}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    media: Mapped[list["Media"]] = relationship(
        "Media", back_populates="user", lazy="raise_on_sql"
    )  #  USER 1:M IMAGE

    user_notification: Mapped[list["User_Notification"]] = relationship(
        "User_Notification", back_populates="user", lazy="raise_on_sql"
    )
    order: Mapped["Order"] = relationship(
        "Order", back_populates="user", lazy="raise_on_sql"
    )
    bucket: Mapped["Bucket"] = relationship(
        "Bucket", back_populates="user", lazy="raise_on_sql"
    )
    promo_code_report: Mapped[list["Promo_Code_Report"]] = relationship(
        "Promo_Code_Report", back_populates="user", lazy="raise_on_sql"
    )
    payment_process: Mapped[list["Payment_Process"]] = relationship(
        "Payment_Process", back_populates="user", lazy="raise_on_sql"
    )
    shop: Mapped[Shop] = relationship(
        "Shop", back_populates="user", lazy="raise_on_sql"
    )  # User 1:1 Shop
    comment: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="user", lazy="raise_on_sql"
    )
    user_address: Mapped[list["User_Address"]] = relationship(
        "User_Address", back_populates="user", lazy="raise_on_sql"
    )
    courier_profile: Mapped["Courier_Profile"] = relationship(
        "Courier_Profile", back_populates="user", lazy="raise_on_sql"
    )  # USER 1:1 COURIER_PROFILE
    wallet: Mapped["Wallet"] = relationship(
        "Wallet", back_populates="user", lazy="raise_on_sql"
    )
    like: Mapped[list["Like"]] = relationship(
        "Like", back_populates="user", lazy="raise_on_sql"
    )
    user_rating: Mapped[list["User_Rating"]] = relationship(
        "User_Rating", back_populates="user", lazy="raise_on_sql"
    )
    user_search: Mapped[list["User_Search"]] = relationship(
        "User_Search", back_populates="user", lazy="raise_on_sql"
    )
    user_session_token: Mapped["UserSessionToken"] = relationship(
        "UserSessionToken", back_populates="user", lazy="raise_on_sql"
    )
    audit_log: Mapped[list["Audit_Log"]] = relationship(
        "Audit_Log", back_populates="user", lazy="raise_on_sql"
    )
    role_request_user: Mapped[list["Role_Request"]] = relationship(
        "Role_Request",
        foreign_keys="Role_Request.user_id",
        back_populates="user",
        lazy="raise_on_sql",
    )
    reviewed_by_admin: Mapped[list["Role_Request"]] = relationship(
        "Role_Request",
        foreign_keys="Role_Request.reviewed_by",
        back_populates="reviewer",
        lazy="raise_on_sql",
    )


class User_Address(BaseMain):
    __tablename__ = "user_address"

    user_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    region_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("region.id", ondelete="SET NULL"), nullable=False
    )
    address: Mapped[str] = mapped_column(String(250), nullable=False)

    def __repr__(self):
        return f"user address: {self.address}"

    user: Mapped["User"] = relationship(
        "User", back_populates="user_address", lazy="raise_on_sql"
    )
    region: Mapped["Region"] = relationship(
        "Region", back_populates="user_address", lazy="raise_on_sql"
    )

    order: Mapped[list["Order"]] = relationship(
        "Order", back_populates="user_address", lazy="raise_on_sql"
    )
    delivery_process: Mapped[list["Delivery_Process"]] = relationship(
        "Delivery_Process", back_populates="user_address", lazy="raise_on_sql"
    )


class Courier_Profile(BaseMain):
    __tablename__ = "courier_profile"

    user_id: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey("user.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    transport_type: Mapped[str] = mapped_column(String(200), default=None)
    unique_number: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    is_ready: Mapped[bool] = mapped_column(Boolean, nullable=True)
    balance: Mapped[float] = mapped_column(Float, default=None)

    def __repr__(self):
        return f"Courier id: {self.user_id}"

    user: Mapped["User"] = relationship(
        "User", back_populates="courier_profile", lazy="raise_on_sql"
    )  # 1:1 relationship with User

    delivery_process: Mapped[list["Delivery_Process"]] = relationship(
        "Delivery_Process", back_populates="courier_profile", lazy="raise_on_sql"
    )


class Wallet(BaseMain):
    __tablename__ = "wallet"

    user_id: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey("user.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    balance: Mapped[float] = mapped_column(Float, default=None)
    currency: Mapped[str] = mapped_column(String(10), default="USD")
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f"Wallet id: {self.user_id}"

    user: Mapped["User"] = relationship(
        "User", back_populates="wallet", lazy="raise_on_sql"
    )
    payment_process: Mapped[list["Payment_Process"]] = relationship(
        "Payment_Process", back_populates="wallet", lazy="raise_on_sql"
    )
    transaction_log: Mapped[list["Transaction_Log"]] = relationship(
        "Transaction_Log", back_populates="wallet", lazy="raise_on_sql"
    )


class Like(BaseMain):
    __tablename__ = "like"
    user_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("product.id", ondelete="CASCADE"), nullable=False
    )

    user: Mapped["User"] = relationship(
        "User", back_populates="like", lazy="raise_on_sql"
    )
    product: Mapped["Product"] = relationship(
        "Product", back_populates="like", lazy="raise_on_sql"
    )


class User_Rating(BaseMain):
    __tablename__ = "user_rating"

    user_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("product.id", ondelete="CASCADE"), nullable=False
    )
    ball: Mapped[int] = mapped_column(SmallInteger, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=True)

    def __repr__(self):
        return f"user rating ball: {self.ball}"

    user: Mapped["User"] = relationship(
        "User", back_populates="user_rating", lazy="raise_on_sql"
    )
    product: Mapped["Product"] = relationship(
        "Product", back_populates="user_rating", lazy="raise_on_sql"
    )


class User_Search(BaseMain):
    __tablename__ = "user_search"

    user_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("product.id", ondelete="CASCADE"), nullable=True
    )
    query_text: Mapped[str] = mapped_column(String(255))

    def __repr__(self):
        return f"user query{self.query_text}"

    user: Mapped["User"] = relationship(
        "User", back_populates="user_search", lazy="raise_on_sql"
    )
    product: Mapped["Product"] = relationship(
        "Product", back_populates="user_search", lazy="raise_on_sql"
    )


class Audit_Log(BaseMain):
    __tablename__ = "audit_log"

    user_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("user.id", ondelete="SET NULL"), nullable=False
    )
    action: Mapped[str] = mapped_column(String(150), nullable=True)
    target_table: Mapped[str] = mapped_column(String(50), nullable=True)
    target_table_id: Mapped[int] = mapped_column(SmallInteger, nullable=True)
    before_data: Mapped[JSON] = mapped_column(JSON, nullable=True)
    after_data: Mapped[JSON] = mapped_column(JSON, nullable=True)

    def __repr__(self):
        return f"user change action: {self.action}, target table:{self.target_table}"

    user: Mapped["User"] = relationship(
        "User", back_populates="audit_log", lazy="raise_on_sql"
    )


class UserSessionToken(BaseMain):
    __tablename__ = "user_session_token"
    user_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    token: Mapped[str] = mapped_column(String(255), nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"user token:{self.token}"

    user: Mapped["User"] = relationship(
        "User", back_populates="user_session_token", lazy="raise_on_sql"
    )


class Role_Request(
    BaseMain
):  # tableni maqsadi active user unchun manager/merchant/courier=true huquqini tastiqlash joyi
    __tablename__ = "role_request"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id", ondelete="SET NULL"), nullable=False
    )
    request_role: Mapped[bool] = mapped_column(Boolean, default="active")
    application: Mapped[Text] = mapped_column(Text, nullable=True)
    resume_url: Mapped[str] = mapped_column(String(250), nullable=True)
    checking_status: Mapped[bool] = mapped_column(Boolean, nullable=True)
    reviewed_by: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )
    reviewed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    status_expired_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    hash_code: Mapped[str] = mapped_column(String(255), nullable=True)
    attempt_count: Mapped[int] = mapped_column(SmallInteger, default=0)

    def __repr__(self):
        return f"user:{self.user_id}, resume:{self.resume_url}"

    user: Mapped["User"] = relationship(
        "User",
        
        foreign_keys=[user_id],
        back_populates="role_request_user",
        lazy="raise_on_sql",
    )
    reviewer: Mapped["User"] = relationship(
        "User",
        foreign_keys=[reviewed_by],
        back_populates="reviewed_by_admin",
        lazy="raise_on_sql",
    )
