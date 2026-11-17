import csv
import random
from datetime import date, timedelta
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

NUMBER_OF_RECORDS = 300
RANDOM_SEED = 42

DATA_DIR = Path(__file__).resolve().parent

OUTPUT_FILE = DATA_DIR / "sales_mock_data.csv"


# ============================================================
# Mock data values
# ============================================================

FIRST_NAMES = [
    "Emma",
    "Oliver",
    "Sofia",
    "Daniel",
    "Laura",
    "Mikko",
    "Anna",
    "John",
    "Maria",
    "Antti",
    "Ella",
    "Samuel",
    "Nora",
    "Lucas",
    "Emilia"
]


LAST_NAMES = [
    "Carter",
    "Smith",
    "Virtanen",
    "Korhonen",
    "Laine",
    "Niemi",
    "Lehto",
    "Johnson",
    "Koski",
    "Makinen"
]


GENDERS = [
    "Female",
    "Male",
    "Other"
]


CUSTOMER_SEGMENTS = [
    "Consumer",
    "Corporate",
    "Small Business"
]


SALES_CHANNELS = [
    "Online",
    "Retail Store",
    "Mobile App"
]


STORE_DATA = [
    {
        "store_id": "HEL-01",
        "store_name": "Helsinki Central Store",
        "country": "Finland",
        "region": "Uusimaa",
        "city": "Helsinki"
    },
    {
        "store_id": "VAN-01",
        "store_name": "Vantaa Store",
        "country": "Finland",
        "region": "Uusimaa",
        "city": "Vantaa"
    },
    {
        "store_id": "TMP-01",
        "store_name": "Tampere Store",
        "country": "Finland",
        "region": "Pirkanmaa",
        "city": "Tampere"
    },
    {
        "store_id": "TKU-01",
        "store_name": "Turku Store",
        "country": "Finland",
        "region": "Varsinais-Suomi",
        "city": "Turku"
    },
    {
        "store_id": "OUL-01",
        "store_name": "Oulu Store",
        "country": "Finland",
        "region": "North Ostrobothnia",
        "city": "Oulu"
    }
]


PRODUCTS = [
    {
        "product_id": "P001",
        "product_name": "AeroBook 14 Laptop",
        "category": "Electronics",
        "subcategory": "Computers",
        "unit_price": 899.00,
        "unit_cost": 700.00
    },
    {
        "product_id": "P002",
        "product_name": "Wireless Headphones",
        "category": "Electronics",
        "subcategory": "Audio",
        "unit_price": 149.90,
        "unit_cost": 85.00
    },
    {
        "product_id": "P003",
        "product_name": "4K Monitor",
        "category": "Electronics",
        "subcategory": "Displays",
        "unit_price": 399.00,
        "unit_cost": 275.00
    },
    {
        "product_id": "P004",
        "product_name": "Mechanical Keyboard",
        "category": "Electronics",
        "subcategory": "Accessories",
        "unit_price": 119.90,
        "unit_cost": 65.00
    },
    {
        "product_id": "P005",
        "product_name": "Office Chair",
        "category": "Home",
        "subcategory": "Furniture",
        "unit_price": 329.00,
        "unit_cost": 210.00
    },
    {
        "product_id": "P006",
        "product_name": "Coffee Machine",
        "category": "Home",
        "subcategory": "Kitchen",
        "unit_price": 249.00,
        "unit_cost": 150.00
    },
    {
        "product_id": "P007",
        "product_name": "Running Shoes",
        "category": "Sports",
        "subcategory": "Footwear",
        "unit_price": 129.00,
        "unit_cost": 70.00
    },
    {
        "product_id": "P008",
        "product_name": "Fitness Watch",
        "category": "Sports",
        "subcategory": "Wearables",
        "unit_price": 219.00,
        "unit_cost": 120.00
    },
    {
        "product_id": "P009",
        "product_name": "Winter Jacket",
        "category": "Clothing",
        "subcategory": "Outerwear",
        "unit_price": 179.00,
        "unit_cost": 90.00
    },
    {
        "product_id": "P010",
        "product_name": "Car Battery Charger",
        "category": "Automotive",
        "subcategory": "Accessories",
        "unit_price": 89.90,
        "unit_cost": 45.00
    }
]


PAYMENT_METHODS = [
    "Credit Card",
    "Debit Card",
    "PayPal",
    "Bank Transfer",
    "Mobile Payment"
]


ORDER_STATUSES = [
    "Completed",
    "Shipped",
    "Processing",
    "Cancelled",
    "Returned"
]


SHIPPING_METHODS = [
    "Standard",
    "Express",
    "Pickup"
]


RETURN_REASONS = [
    "Damaged",
    "Wrong Product",
    "Defective",
    "Customer Return"
]


SALES_REPRESENTATIVES = [
    "John Miller",
    "Emma Wilson",
    "Laura Brown",
    "Daniel Anderson",
    "Sofia Martin"
]


PROMOTION_CODES = [
    "",
    "",
    "",
    "WINTER10",
    "SAVE15",
    "WELCOME5"
]


# ============================================================
# Helper functions
# ============================================================

def generate_random_date():
    start_date = date(2024, 1, 1)
    end_date = date(2026, 10, 31)

    day_range = (
        end_date - start_date
    ).days

    return start_date + timedelta(
        days=random.randint(
            0,
            day_range
    )
)


def generate_random_time():
    hour = random.randint(8, 21)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    return (
        f"{hour:02d}:"
        f"{minute:02d}:"
        f"{second:02d}"
    )


def get_storage_type(index):
    """
    Divide the 300 records into three equal partitions.

    Records 1-100:
    PostgreSQL only.

    Records 101-200:
    MongoDB only.

    Records 201-300:
    Stored in both databases.
    """

    if index <= 100:
        return "SQL_ONLY"

    if index <= 200:
        return "NOSQL_ONLY"

    return "SHARED"


# ============================================================
# Customer generation
# ============================================================

def generate_customers(customer_count=100):
    customers = []

    for index in range(
        1,
        customer_count + 1
    ):
        first_name = random.choice(
            FIRST_NAMES
        )

        last_name = random.choice(
            LAST_NAMES
        )

        customer = {
            "customer_id":
                f"C{index:05d}",

            "customer_name":
                f"{first_name} {last_name}",

            "customer_age":
                random.randint(
                    18,
                    80
                ),

            "customer_gender":
                random.choice(
                    GENDERS
                ),

            "customer_segment":
                random.choice(
                    CUSTOMER_SEGMENTS
                )
        }

        customers.append(customer)

    return customers


# ============================================================
# Transaction generation
# ============================================================

def generate_transaction(
    index,
    customers
):
    customer = random.choice(
        customers
    )

    product = random.choice(
        PRODUCTS
    )

    store = random.choice(
        STORE_DATA
    )

    order_date = generate_random_date()

    quantity = random.randint(
        1,
        5
    )

    discount_percentage = random.choice(
        [
            0,
            0,
            0,
            5,
            10,
            15,
            20
        ]
    )

    gross_sales = (
        quantity
        * product["unit_price"]
    )

    discount_multiplier = (
        1
        - discount_percentage / 100
    )

    sales_amount = round(
        gross_sales
        * discount_multiplier,
        2
    )

    cost_amount = round(
        quantity
        * product["unit_cost"],
        2
    )

    profit = round(
        sales_amount
        - cost_amount,
        2
    )

    order_status = random.choices(
        ORDER_STATUSES,
        weights=[
            60,
            15,
            10,
            5,
            10
        ],
        k=1
    )[0]

    if order_status == "Returned":
        return_flag = "Y"

        return_reason = random.choice(
        RETURN_REASONS
        )
    else:
        return_flag = "N"
        return_reason = ""

    delivery_days = random.randint(
        1,
        10
    )

    customer_rating = random.choice(
        [
            1,
            2,
            3,
            4,
            4,
            5,
            5
        ]
    )

    inventory_level = random.randint(
        0,
        500
    )

    storage_type = get_storage_type(
        index
    )

    return {
        "Transaction_ID":
            f"T{20000000 + index}",

        "Order_ID":
            f"O{1000000 + index}",

        "Customer_ID":
            customer["customer_id"],

        "Customer_Name":
            customer["customer_name"],

        "Customer_Age":
            customer["customer_age"],

        "Customer_Gender":
            customer["customer_gender"],

        "Customer_Segment":
            customer["customer_segment"],

        "Order_Date":
            order_date.isoformat(),

        "Order_Time":
            generate_random_time(),

        "Sales_Channel":
            random.choice(
                SALES_CHANNELS
            ),

        "Store_ID":
            store["store_id"],

        "Store_Name":
            store["store_name"],

        "Country":
            store["country"],

        "Region":
            store["region"],

        "City":
            store["city"],

        "Product_ID":
            product["product_id"],

        "Product_Name":
            product["product_name"],

        "Product_Category":
            product["category"],

        "Product_Subcategory":
            product["subcategory"],

        "Quantity":
            quantity,

        "Unit_Price":
            f"{product['unit_price']:.2f}",

        "Discount_Percentage":
            discount_percentage,

        "Sales_Amount":
            f"{sales_amount:.2f}",

        "Cost_Amount":
            f"{cost_amount:.2f}",

        "Profit":
            f"{profit:.2f}",

        "Payment_Method":
            random.choice(
                PAYMENT_METHODS
            ),

        "Order_Status":
            order_status,

        "Shipping_Method":
            random.choice(
                SHIPPING_METHODS
            ),

        "Delivery_Days":
            delivery_days,

        "Return_Flag":
            return_flag,

        "Return_Reason":
            return_reason,

        "Sales_Representative":
            random.choice(
                SALES_REPRESENTATIVES
            ),

        "Promotion_Code":
            random.choice(
                PROMOTION_CODES
            ),

        "Customer_Rating":
            customer_rating,

        "Inventory_Level":
            inventory_level,

        "Order_Year":
            order_date.year,

        # System metadata used for database partitioning.
        "Storage_Type":
            storage_type,

        # Used later by the replication protocol.
        "Version":
            1
    }


# ============================================================
# Dataset generation
# ============================================================

def generate_dataset():
    random.seed(
        RANDOM_SEED
    )

    customers = generate_customers(
        customer_count=100
    )

    records = []

    for index in range(
        1,
        NUMBER_OF_RECORDS + 1
    ):
        transaction = generate_transaction(
            index,
            customers
        )

        records.append(transaction)

    return records


# ============================================================
# Dataset validation
# ============================================================

def validate_dataset(records):
    sql_only_count = sum(
        record["Storage_Type"]
        == "SQL_ONLY"
        for record in records
    )

    nosql_only_count = sum(
        record["Storage_Type"]
        == "NOSQL_ONLY"
        for record in records
    )

    shared_count = sum(
        record["Storage_Type"]
        == "SHARED"
        for record in records
    )

    transaction_ids = {
        record["Transaction_ID"]
        for record in records
    }

    print()
    print("Dataset validation")
    print("------------------")

    print(
        f"Total records: {len(records)}"
    )

    print(
        f"Unique transaction IDs: "
        f"{len(transaction_ids)}"
    )

    print(
        f"SQL_ONLY: {sql_only_count}"
    )

    print(
        f"NOSQL_ONLY: {nosql_only_count}"
    )

    print(
        f"SHARED: {shared_count}"
    )

    if len(records) != NUMBER_OF_RECORDS:
        raise ValueError(
            "Incorrect total number of records."
        )

    if (
    len(transaction_ids)
    != NUMBER_OF_RECORDS
    ):
        raise ValueError(
        "Transaction IDs are not unique."
    )

    expected_partition_size = (
        NUMBER_OF_RECORDS // 3
    )

    if (
        sql_only_count
        != expected_partition_size
    ):
        raise ValueError(
            "SQL_ONLY partition size "
            "is incorrect."
        )

    if (
        nosql_only_count
        != expected_partition_size
    ):
        raise ValueError(
            "NOSQL_ONLY partition size "
            "is incorrect."
        )

    if (
        shared_count
        != expected_partition_size
    ):
        raise ValueError(
            "SHARED partition size "
            "is incorrect."
        )


# ============================================================
# CSV output
# ============================================================

def save_csv(records):
    if not records:
        raise ValueError(
            "No records were generated."
        )

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    fieldnames = list(
        records[0].keys()
    )

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(
            records
        )


# ============================================================
# Main
# ============================================================

def main():
    print(
        "Generating synthetic sales data..."
    )

    print(
        f"Random seed: {RANDOM_SEED}"
    )

    records = generate_dataset()

    validate_dataset(
        records
    )

    save_csv(
        records
    )

    print()
    print(
        "Synthetic dataset created "
        "successfully."
    )

    print(
        f"Output file: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
