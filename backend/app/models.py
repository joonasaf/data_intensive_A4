from datetime import date, time

from sqlalchemy import (
    Date,
    Integer,
    Numeric,
    String,
    Time
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import SqlBase


class SalesTransaction(SqlBase):
    __tablename__ = "sales_transactions"

    transaction_id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True
    )

    order_id: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    customer_id: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    customer_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    customer_age: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    customer_gender: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    customer_segment: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    order_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    order_time: Mapped[time] = mapped_column(
        Time,
        nullable=False
    )

    sales_channel: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    store_id: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    store_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    country: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    region: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    product_id: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    product_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    product_category: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    product_subcategory: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    unit_price: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    discount_percentage: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False
    )

    sales_amount: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    cost_amount: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    profit: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    payment_method: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    order_status: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    shipping_method: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    delivery_days: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    return_flag: Mapped[str] = mapped_column(
        String(1),
        nullable=False
    )

    return_reason: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    sales_representative: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    promotion_code: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    customer_rating: Mapped[float] = mapped_column(
        Numeric(3, 1),
        nullable=False
    )

    inventory_level: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    order_year: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    # Application metadata

    storage_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1
    )
