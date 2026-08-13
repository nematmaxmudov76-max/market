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
    from .user import User, Wallet
    from .order import Order


class Payment_Process(BaseMain):
    __tablename__ = "payment_process"

    user_id:Mapped[int] = mapped_column(SmallInteger, ForeignKey("user.id", ondelete="SET NULL"), nullable=False)
    order_id:Mapped[int] = mapped_column(SmallInteger, ForeignKey("order.id", ondelete="SET NULL"), nullable=False)
    wallet_id:Mapped[int] = mapped_column(SmallInteger, ForeignKey("wallet.id", ondelete="SET NULL"), nullable=False)
    total_amount:Mapped[float] = mapped_column(Float, default=None)
    status:Mapped[str] = mapped_column(String(100), default="pending")

    def __repr__(self):
        return f"user id: {self.user_id}, order id: {self.order_id}, wallet id: {self.wallet_id}, total amount: {self.total_amount}, status: {self.status}"

    user:Mapped["User"] = relationship("User", back_populates="payment_process", lazy="raise_on_sql")
    order:Mapped["Order"] = relationship("Order", back_populates="payment_process", lazy="raise_on_sql")
    wallet:Mapped["Wallet"] = relationship("Wallet", back_populates="payment_process", lazy="raise_on_sql")
    transaction_log:Mapped[list["Transaction_Log"]] = relationship("Transaction_Log", back_populates="payment_process", lazy="raise_on_sql")

class Transaction_Log(BaseMain):
    __tablename__ = "transaction_log"

    payment_id:Mapped[int] = mapped_column(SmallInteger, ForeignKey("payment_process.id", ondelete="SET NULL"), nullable=False)
    wallet_id:Mapped[int] = mapped_column(SmallInteger, ForeignKey("wallet.id", ondelete="SET NULL"), nullable=False)
    status:Mapped[str] = mapped_column(String(100), default="pending")
    transaction_params:Mapped[str] = mapped_column(Text, default=None)

    def __repr__(self):
        return f"payment id: {self.payment_id}, wallet id: {self.wallet_id}, status: {self.status}, transaction params: {self.transaction_params}"

    payment_process:Mapped["Payment_Process"] = relationship("Payment_Process", back_populates="transaction_log", lazy="raise_on_sql")
    wallet:Mapped["Wallet"] = relationship("Wallet", back_populates="transaction_log", lazy="raise_on_sql")