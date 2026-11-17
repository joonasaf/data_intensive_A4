import csv
from datetime import date, time
from decimal import Decimal
from pathlib import Path

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.database import (
    SqlSessionLocal,
    mongo_collection
)

from app.models import SalesTransaction


# ============================================================
# File locations
# ============================================================

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BACKEND_DIR.parent

DATA_FILE = (
PROJECT_DIR
    / "data"
    / "sales_mock_data.csv"
)


# ============================================================
# Expected dataset sizes
# ============================================================

EXPECTED_TOTAL_RECORDS = 300
EXPECTED_PARTITION_SIZE = 100

EXPECTED_SQL_RECORDS = 200
EXPECTED_MONGODB_RECORDS = 200


# ============================================================
# Type conversion helpers
# ============================================================

def parse_integer(value: str) -> int:
    return int(value)


def parse_decimal(value: str) -> Decimal:
    return Decimal(value)


def parse_date(value: str) -> date:
    return date.fromisoformat(value)


def parse_time(value: str) -> time:
    return time.fromisoformat(value)


def empty_string_to_none(
    value: str
) -> str | None:
    stripped_value = value.strip()

    if stripped_value == "":
        return None

    return stripped_value


# ============================================================
# CSV validation
# ============================================================

def validate_csv_file():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            "Mock data file was not found: "
            f"{DATA_FILE}"
        )

    if not DATA_FILE.is_file():
        raise ValueError(
            "The configured data path is not a file: "
            f"{DATA_FILE}"
        )


def validate_csv_records(records: list[dict[str, str]]):
    if len(records) != EXPECTED_TOTAL_RECORDS:
        raise ValueError(
            "The CSV must contain exactly "
            f"{EXPECTED_TOTAL_RECORDS} records, "
            f"but it contains {len(records)}."
        )

    transaction_ids = {
        record["Transaction_ID"]
        for record in records
    }

    if len(transaction_ids) != EXPECTED_TOTAL_RECORDS:
        raise ValueError(
            "Transaction_ID values are not unique."
        )

    sql_only_count = sum(
        record["Storage_Type"] == "SQL_ONLY"
        for record in records
    )

    nosql_only_count = sum(
        record["Storage_Type"] == "NOSQL_ONLY"
        for record in records
    )

    shared_count = sum(
        record["Storage_Type"] == "SHARED"
        for record in records
    )

    if sql_only_count != EXPECTED_PARTITION_SIZE:
        raise ValueError(
            "Incorrect SQL_ONLY partition size: "
            f"{sql_only_count}"
        )

    if nosql_only_count != EXPECTED_PARTITION_SIZE:
        raise ValueError(
            "Incorrect NOSQL_ONLY partition size: "
            f"{nosql_only_count}"
        )

    if shared_count != EXPECTED_PARTITION_SIZE:
        raise ValueError(
            "Incorrect SHARED partition size: "
            f"{shared_count}"
        )

    print()
    print("CSV validation")
    print("--------------")
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


# ============================================================
# CSV reading
# ============================================================

def read_csv_records() -> list[dict[str, str]]:
    validate_csv_file()

    with DATA_FILE.open(
        "r",
        newline="",
        encoding="utf-8"
    ) as csv_file:
        reader = csv.DictReader(csv_file)

        records = list(reader)

    validate_csv_records(records)

    return records


# ============================================================
# PostgreSQL conversion
# ============================================================

def create_sql_record(
    csv_record: dict[str, str]
) -> SalesTransaction:
    return SalesTransaction(
        transaction_id=
            csv_record["Transaction_ID"],

        order_id=
            csv_record["Order_ID"],

        customer_id=
            csv_record["Customer_ID"],

        customer_name=
        csv_record["Customer_Name"],

        customer_age=parse_integer(
            csv_record["Customer_Age"]
        ),

        customer_gender=
            csv_record["Customer_Gender"],

        customer_segment=
            csv_record["Customer_Segment"],

        order_date=parse_date(
            csv_record["Order_Date"]
        ),

        order_time=parse_time(
            csv_record["Order_Time"]
        ),

        sales_channel=
            csv_record["Sales_Channel"],

        store_id=
            csv_record["Store_ID"],

        store_name=
            csv_record["Store_Name"],

        country=
            csv_record["Country"],

        region=
            csv_record["Region"],

        city=
            csv_record["City"],

        product_id=
            csv_record["Product_ID"],

        product_name=
            csv_record["Product_Name"],

        product_category=
            csv_record["Product_Category"],

        product_subcategory=
            csv_record["Product_Subcategory"],

        quantity=parse_integer(
            csv_record["Quantity"]
        ),

        unit_price=parse_decimal(
            csv_record["Unit_Price"]
        ),

        discount_percentage=parse_decimal(
            csv_record["Discount_Percentage"]
        ),

        sales_amount=parse_decimal(
            csv_record["Sales_Amount"]
        ),

        cost_amount=parse_decimal(
            csv_record["Cost_Amount"]
        ),

        profit=parse_decimal(
            csv_record["Profit"]
        ),

        payment_method=
            csv_record["Payment_Method"],

        order_status=
            csv_record["Order_Status"],

        shipping_method=
            csv_record["Shipping_Method"],

        delivery_days=parse_integer(
            csv_record["Delivery_Days"]
        ),

        return_flag=
            csv_record["Return_Flag"],

        return_reason=empty_string_to_none(
            csv_record["Return_Reason"]
        ),

        sales_representative=
            csv_record["Sales_Representative"],

        promotion_code=empty_string_to_none(
            csv_record["Promotion_Code"]
        ),

        customer_rating=parse_decimal(
            csv_record["Customer_Rating"]
        ),

        inventory_level=parse_integer(
            csv_record["Inventory_Level"]
        ),

        order_year=parse_integer(
            csv_record["Order_Year"]
        ),

        storage_type=
            csv_record["Storage_Type"],

        version=parse_integer(
            csv_record["Version"]
        )
    )


# ============================================================
# MongoDB conversion
# ============================================================

def create_mongodb_document(
    csv_record: dict[str, str]
) -> dict:
    transaction_id = csv_record[
        "Transaction_ID"
    ]

    return {
        # Transaction_ID is also used as the MongoDB
        # document identifier. This prevents duplicates.
        "_id": transaction_id,

        "transaction_id":
            transaction_id,

        "order_id":
            csv_record["Order_ID"],

        "customer_id":
            csv_record["Customer_ID"],

        "customer_name":
            csv_record["Customer_Name"],

        "customer_age": parse_integer(
            csv_record["Customer_Age"]
        ),

        "customer_gender":
            csv_record["Customer_Gender"],

        "customer_segment":
            csv_record["Customer_Segment"],

        # ISO strings are easy to return through FastAPI
        # and display in React.
        "order_date":
            csv_record["Order_Date"],

        "order_time":
            csv_record["Order_Time"],

        "sales_channel":
            csv_record["Sales_Channel"],

        "store_id":
            csv_record["Store_ID"],

        "store_name":
            csv_record["Store_Name"],

        "country":
            csv_record["Country"],

        "region":
            csv_record["Region"],

        "city":
            csv_record["City"],

        "product_id":
            csv_record["Product_ID"],

        "product_name":
            csv_record["Product_Name"],

        "product_category":
            csv_record["Product_Category"],

        "product_subcategory":
            csv_record["Product_Subcategory"],

        "quantity": parse_integer(
            csv_record["Quantity"]
        ),

        "unit_price": float(
            csv_record["Unit_Price"]
        ),

        "discount_percentage": float(
            csv_record["Discount_Percentage"]
        ),

        "sales_amount": float(
            csv_record["Sales_Amount"]
        ),

        "cost_amount": float(
            csv_record["Cost_Amount"]
        ),

        "profit": float(
            csv_record["Profit"]
        ),

        "payment_method":
            csv_record["Payment_Method"],

        "order_status":
            csv_record["Order_Status"],

        "shipping_method":
            csv_record["Shipping_Method"],

        "delivery_days": parse_integer(
            csv_record["Delivery_Days"]
        ),

        "return_flag":
            csv_record["Return_Flag"],

        "return_reason": empty_string_to_none(
            csv_record["Return_Reason"]
        ),

        "sales_representative":
            csv_record["Sales_Representative"],

        "promotion_code": empty_string_to_none(
            csv_record["Promotion_Code"]
        ),

        "customer_rating": float(
            csv_record["Customer_Rating"]
        ),

        "inventory_level": parse_integer(
            csv_record["Inventory_Level"]
        ),

        "order_year": parse_integer(
            csv_record["Order_Year"]
        ),

        "storage_type":
            csv_record["Storage_Type"],

        "version": parse_integer(
            csv_record["Version"]
        )
    }


# ============================================================
# Existing data reset
# ============================================================

def clear_postgresql_data(
    database: Session
):
    print(
        "Clearing PostgreSQL data..."
    )

    database.execute(
        delete(SalesTransaction)
    )

    database.commit()


def clear_mongodb_data():
    print(
        "Clearing MongoDB data..."
    )

    mongo_collection.delete_many({})


# ============================================================
# Import
# ============================================================

def import_records(
    records: list[dict[str, str]]
):
    sql_database = SqlSessionLocal()

    sql_records = []
    mongodb_documents = []

    sql_only_count = 0
    nosql_only_count = 0
    shared_count = 0

    try:
        clear_postgresql_data(
            sql_database
        )

        clear_mongodb_data()

        for csv_record in records:
            storage_type = csv_record[
                "Storage_Type"
            ]

            if storage_type == "SQL_ONLY":
                sql_records.append(
                    create_sql_record(
                        csv_record
                    )
                )

                sql_only_count += 1

            elif storage_type == "NOSQL_ONLY":
                mongodb_documents.append(
                    create_mongodb_document(
                        csv_record
                    )
                )

                nosql_only_count += 1

            elif storage_type == "SHARED":
                sql_records.append(
                    create_sql_record(
                        csv_record
                    )
                )

                mongodb_documents.append(
                    create_mongodb_document(
                        csv_record
                    )
                )

                shared_count += 1

            else:
                raise ValueError(
                    "Unknown Storage_Type: "
                    f"{storage_type}"
                )

        print(
            "Writing records to PostgreSQL..."
        )

        sql_database.add_all(
            sql_records
        )

        sql_database.commit()

        print(
            "Writing documents to MongoDB..."
        )

        if mongodb_documents:
            mongo_collection.insert_many(
                mongodb_documents,
                ordered=True
            )

        print()
        print("Import operations")
        print("-----------------")
        print(
            f"SQL_ONLY processed: "
            f"{sql_only_count}"
        )
        print(
            f"NOSQL_ONLY processed: "
            f"{nosql_only_count}"
        )
        print(
            f"SHARED processed: "
            f"{shared_count}"
        )

    except Exception:
        sql_database.rollback()

        print()
        print(
            "Import failed. PostgreSQL transaction was rolled back."
        )

        raise

    finally:
        sql_database.close()


# ============================================================
# Import validation
# ============================================================

def validate_postgresql():
    database = SqlSessionLocal()

    try:
        total_count = database.scalar(
            select(
                func.count(
                    SalesTransaction.transaction_id
                )
            )
        )

        sql_only_count = database.scalar(
            select(
                func.count(
                    SalesTransaction.transaction_id
                )
            ).where(
                SalesTransaction.storage_type
                == "SQL_ONLY"
            )
        )

        shared_count = database.scalar(
            select(
                func.count(
                    SalesTransaction.transaction_id
                )
            ).where(
                SalesTransaction.storage_type
                == "SHARED"
            )
        )

        return {
            "total": total_count or 0,
            "sql_only": sql_only_count or 0,
            "shared": shared_count or 0
        }

    finally:
        database.close()


def validate_mongodb():
    total_count = (
        mongo_collection.count_documents({})
    )

    nosql_only_count = (
        mongo_collection.count_documents({
            "storage_type": "NOSQL_ONLY"
        })
    )

    shared_count = (
        mongo_collection.count_documents({
            "storage_type": "SHARED"
        })
    )

    return {
        "total": total_count,
        "nosql_only": nosql_only_count,
        "shared": shared_count
    }


def validate_shared_replication():
    sql_database = SqlSessionLocal()

    try:
        sql_shared_ids = set(
            sql_database.scalars(
                select(
                    SalesTransaction.transaction_id
                ).where(
                    SalesTransaction.storage_type
                    == "SHARED"
                )
            ).all()
        )

    finally:
        sql_database.close()

    mongodb_shared_ids = {
        document["transaction_id"]
        for document in mongo_collection.find(
            {
                "storage_type": "SHARED"
            },
            {
                "_id": 0,
                "transaction_id": 1
            }
        )
    }

    missing_from_mongodb = (
        sql_shared_ids
        - mongodb_shared_ids
    )

    missing_from_postgresql = (
        mongodb_shared_ids
        - sql_shared_ids
    )

    return {
        "sql_shared_count":
            len(sql_shared_ids),

        "mongodb_shared_count":
            len(mongodb_shared_ids),

        "missing_from_mongodb":
            missing_from_mongodb,

        "missing_from_postgresql":
            missing_from_postgresql
    }


def print_validation_results():
    postgresql_result = (
        validate_postgresql()
    )

    mongodb_result = (
        validate_mongodb()
    )

    replication_result = (
        validate_shared_replication()
    )

    print()
    print("Database validation")
    print("-------------------")

    print()
    print("PostgreSQL")
    print(
        f" SQL_ONLY: "
        f"{postgresql_result['sql_only']}"
    )
    print(
        f" SHARED: "
        f"{postgresql_result['shared']}"
    )
    print(
        f" Total: "
        f"{postgresql_result['total']}"
    )

    print()
    print("MongoDB")
    print(
        f" NOSQL_ONLY: "
        f"{mongodb_result['nosql_only']}"
    )
    print(
        f" SHARED: "
        f"{mongodb_result['shared']}"
    )
    print(
        f" Total: "
        f"{mongodb_result['total']}"
    )

    print()
    print("Shared record validation")
    print(
        f" PostgreSQL SHARED: "
        f"{replication_result['sql_shared_count']}"
    )
    print(
        f" MongoDB SHARED: "
        f"{replication_result['mongodb_shared_count']}"
    )

    missing_from_mongodb = (
        replication_result[
            "missing_from_mongodb"
        ]
    )

    missing_from_postgresql = (
        replication_result[
            "missing_from_postgresql"
        ]
    )

    if (
        missing_from_mongodb
        or missing_from_postgresql
    ):
        raise ValueError(
            "Shared records do not match between "
            "PostgreSQL and MongoDB."
        )

    if (
        postgresql_result["total"]
        != EXPECTED_SQL_RECORDS
    ):
        raise ValueError(
            "Incorrect PostgreSQL record count."
        )

    if (
        mongodb_result["total"]
        != EXPECTED_MONGODB_RECORDS
    ):
        raise ValueError(
            "Incorrect MongoDB document count."
        )

    if (
        postgresql_result["sql_only"]
        != EXPECTED_PARTITION_SIZE
    ):
        raise ValueError(
            "Incorrect SQL_ONLY record count."
        )

    if (
        mongodb_result["nosql_only"]
        != EXPECTED_PARTITION_SIZE
    ):
        raise ValueError(
            "Incorrect NOSQL_ONLY document count."
        )

    if (
        postgresql_result["shared"]
        != EXPECTED_PARTITION_SIZE
    ):
        raise ValueError(
            "Incorrect PostgreSQL SHARED count."
        )

    if (
        mongodb_result["shared"]
        != EXPECTED_PARTITION_SIZE
    ):
        raise ValueError(
            "Incorrect MongoDB SHARED count."
        )

    print()
    print(
        "Database partition validation successful."
    )


# ============================================================
# Main
# ============================================================

def main():
    print("Starting data import")
    print("====================")
    print(
        f"Input file: {DATA_FILE}"
    )

    records = read_csv_records()

    import_records(records)

    print_validation_results()

    print()
    print("Data import completed successfully.")


if __name__ == "__main__":
    main()
