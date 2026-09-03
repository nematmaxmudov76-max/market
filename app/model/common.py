from __future__ import annotations
from app.database import Base
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
from app.model.base import BaseMain
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .user import User, User_Address
    from .order import Order


class Region(BaseMain):
    __tablename__ = "region"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    country_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("country.id", ondelete="SET NULL"), nullable=False
    )

    def __repr__(self):
        return f"region name: {self.name}"

    country: Mapped["Country"] = relationship(
        "Country", back_populates="region", lazy="raise_on_sql"
    )
    user_address: Mapped[list["User_Address"]] = relationship(
        "User_Address", back_populates="region", lazy="raise_on_sql"
    )


class Country(BaseMain):
    __tablename__ = "country"

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    def __repr__(self):
        return f"country name: {self.name}"

    region: Mapped[list["Region"]] = relationship(
        "Region", back_populates="country", lazy="raise_on_sql"
    )


class Notification(BaseMain):
    __tablename__ = "notification"

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(100), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)

    def __repr__(self):
        return f"notification title: {self.title}, type: {self.type}"

    user_notification: Mapped[list["User_Notification"]] = relationship(
        "User_Notification", back_populates="notification", lazy="raise_on_sql"
    )


class User_Notification(BaseMain):
    __tablename__ = "user_notification"

    user_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    notification_id: Mapped[int] = mapped_column(
        SmallInteger, ForeignKey("notification.id", ondelete="CASCADE"), nullable=False
    )
    read_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=None)

    def __repr__(self):
        return f"user id:{self.user_id}, notification id:{self.notification_id}"

    user: Mapped[list["User"]] = relationship(
        "User", back_populates="user_notification", lazy="raise_on_sql"
    )
    notification: Mapped[list["Notification"]] = relationship(
        "Notification", back_populates="user_notification", lazy="raise_on_sql"
    )
