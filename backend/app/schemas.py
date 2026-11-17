from datetime import date, time


from pydantic import BaseModel, ConfigDict, Field




# ------------------------------------------------
# Transaction fields
# ------------------------------------------------


class SalesTransactionBase(BaseModel):
    order_id: str = Field(
        min_length=1,
        max_length=20
    )


    customer_id: str = Field(
        min_length=1,
        max_length=20
    )


    customer_name: str = Field(
        min_length=1,
        max_length=150
    )


    customer_age: int = Field(
        ge=0,
        le=120
    )


    customer_gender: str = Field(
        min_length=1,
        max_length=20
    )


    customer_segment: str = Field(
        min_length=1,
        max_length=50
    )


    order_date: date


    order_time: time


    sales_channel: str = Field(
        min_length=1,
        max_length=50
    )


    store_id: str = Field(
        min_length=1,
        max_length=20
    )


    store_name: str = Field(
        min_length=1,
        max_length=150
    )


    country: str = Field(
        min_length=1,
        max_length=100
    )


    region: str = Field(
        min_length=1,
        max_length=100
    )


    city: str = Field(
        min_length=1,
        max_length=100
    )


    product_id: str = Field(
        min_length=1,
        max_length=20
    )


    product_name: str = Field(
        min_length=1,
        max_length=150
    )


    product_category: str = Field(
        min_length=1,
        max_length=100
    )


    product_subcategory: str = Field(
        min_length=1,
        max_length=100
    )


    quantity: int = Field(
        ge=1
    )


    unit_price: float = Field(
        ge=0
    )


    discount_percentage: float = Field(
        ge=0,
        le=100
    )


    sales_amount: float = Field(
        ge=0
    )


    cost_amount: float = Field(
        ge=0
    )


    profit: float


    payment_method: str = Field(
        min_length=1,
        max_length=50
    )


    order_status: str = Field(
        min_length=1,
        max_length=30
    )


    shipping_method: str = Field(
        min_length=1,
        max_length=30
    )


    delivery_days: int = Field(
        ge=0
    )


    return_flag: str = Field(
        min_length=1,
        max_length=1
    )


    return_reason: str | None = None


    sales_representative: str = Field(
        min_length=1,
        max_length=150
    )


    promotion_code: str | None = None


    customer_rating: float = Field(
        ge=1,
        le=5
    )


    inventory_level: int = Field(
        ge=0
    )


    order_year: int = Field(
        ge=2000,
        le=2100
    )




# ------------------------------------------------
# Update model
# ------------------------------------------------


class SalesTransactionUpdate(BaseModel):
    order_id: str | None = Field(
        default=None,
        min_length=1,
        max_length=20
    )


    customer_id: str | None = Field(
        default=None,
        min_length=1,
        max_length=20
    )


    customer_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150
    )


    customer_age: int | None = Field(
        default=None,
        ge=0,
        le=120
    )


    customer_gender: str | None = Field(
        default=None,
        min_length=1,
        max_length=20
    )


    customer_segment: str | None = Field(
        default=None,
        min_length=1,
        max_length=50
    )


    order_date: date | None = None
    order_time: time | None = None


    sales_channel: str | None = Field(
        default=None,
        min_length=1,
        max_length=50
    )


    store_id: str | None = Field(
        default=None,
        min_length=1,
        max_length=20
    )


    store_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150
    )


    country: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )


    region: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )


    city: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )


    product_id: str | None = Field(
        default=None,
        min_length=1,
        max_length=20
    )


    product_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150
    )


    product_category: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )


    product_subcategory: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )


    quantity: int | None = Field(
        default=None,
        ge=1
    )


    unit_price: float | None = Field(
        default=None,
        ge=0
    )


    discount_percentage: float | None = Field(
        default=None,
        ge=0,
        le=100
    )


    sales_amount: float | None = Field(
        default=None,
        ge=0
    )


    cost_amount: float | None = Field(
        default=None,
        ge=0
    )


    profit: float | None = None


    payment_method: str | None = Field(
        default=None,
        min_length=1,
        max_length=50
    )


    order_status: str | None = Field(
        default=None,
        min_length=1,
        max_length=30
    )


    shipping_method: str | None = Field(
        default=None,
        min_length=1,
        max_length=30
    )


    delivery_days: int | None = Field(
        default=None,
        ge=0
    )


    return_flag: str | None = Field(
        default=None,
        min_length=1,
        max_length=1
    )


    return_reason: str | None = None


    sales_representative: str | None = Field(
        default=None,
        min_length=1,
        max_length=150
    )


    promotion_code: str | None = None


    customer_rating: float | None = Field(
        default=None,
        ge=1,
        le=5
    )


    inventory_level: int | None = Field(
        default=None,
        ge=0
    )


    order_year: int | None = Field(
        default=None,
        ge=2000,
        le=2100
    )




# ------------------------------------------------
# API response
# ------------------------------------------------


class SalesTransactionResponse(
    SalesTransactionBase
):
    model_config = ConfigDict(
        from_attributes=True
    )


    transaction_id: str


    storage_type: str


    version: int


    source: str | None = None


    sql_version: int | None = None


    nosql_version: int | None = None


    replication_status: str | None = None
