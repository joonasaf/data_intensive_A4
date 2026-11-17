from sqlalchemy import String, cast, or_, select
from sqlalchemy.orm import Session

from app.database import mongo_collection
from app.models import SalesTransaction
import re

#------------------------------------------------
# Constants
#------------------------------------------------

DEFAULT_LIMIT = 100
MAX_LIMIT = 500

#------------------------------------------------
# Helpers
#------------------------------------------------

def normalize_limit(limit: int) -> int:
    try:
        numeric_limit = int(limit)
    except (TypeError, ValueError):
        return DEFAULT_LIMIT

    if numeric_limit < 1:
        return DEFAULT_LIMIT

    return min(
        numeric_limit,
        MAX_LIMIT
    )

def sql_record_to_dict(record: SalesTransaction) -> dict:
    return {
        "transaction_id":
            record.transaction_id,

        "order_id":
            record.order_id,

        "customer_id":
            record.customer_id,

        "customer_name":
            record.customer_name,

        "customer_age":
            record.customer_age,

        "customer_gender":
            record.customer_gender,

        "customer_segment":
            record.customer_segment,

        "order_date":
            record.order_date.isoformat(),

        "order_time":
            record.order_time.isoformat(),

        "sales_channel":
            record.sales_channel,

        "store_id":
            record.store_id,

        "store_name":
            record.store_name,

        "country":
            record.country,

        "region":
            record.region,

        "city":
            record.city,

        "product_id":
            record.product_id,

        "product_name":
            record.product_name,

        "product_category":
            record.product_category,

        "product_subcategory":
            record.product_subcategory,

        "quantity":
            record.quantity,

        "unit_price":
            float(record.unit_price),

        "discount_percentage":
            float(record.discount_percentage),

        "sales_amount":
            float(record.sales_amount),

        "cost_amount":
            float(record.cost_amount),

        "profit":
            float(record.profit),

        "payment_method":
            record.payment_method,

        "order_status":
            record.order_status,

        "shipping_method":
            record.shipping_method,

        "delivery_days":
            record.delivery_days,

        "return_flag":
            record.return_flag,

        "return_reason":
            record.return_reason,

        "sales_representative":
            record.sales_representative,

        "promotion_code":
            record.promotion_code,

        "customer_rating":
            float(record.customer_rating),

        "inventory_level":
            record.inventory_level,

        "order_year":
            record.order_year,

        "storage_type":
            record.storage_type,

        "version":
            record.version
    }


def mongodb_document_to_dict(document: dict) -> dict:
    result = dict(document)

    # MongoDB's internal _id should not be returned
    # separately because transaction_id is the
    # application-level identifier.
    result.pop("_id",None)

    return result


#------------------------------------------------
# PostgreSQL search
#------------------------------------------------

def search_postgresql(
    database: Session,
    search_term: str = "",
    limit: int = DEFAULT_LIMIT
) -> list[dict]:

    safe_limit = normalize_limit(
        limit
    )

    cleaned_search_term = (
        search_term.strip()
    )

    statement = select(
        SalesTransaction
    )

    if cleaned_search_term:
        search_pattern = (
            f"%{cleaned_search_term}%"
        )

        statement = statement.where(
            or_(
                SalesTransaction.transaction_id
                .ilike(search_pattern),

                SalesTransaction.order_id
                .ilike(search_pattern),

                SalesTransaction.customer_id
                .ilike(search_pattern),

                SalesTransaction.customer_name
                .ilike(search_pattern),

                SalesTransaction.customer_gender
                .ilike(search_pattern),

                SalesTransaction.customer_segment
                .ilike(search_pattern),

                SalesTransaction.sales_channel
                .ilike(search_pattern),

                SalesTransaction.store_id
                .ilike(search_pattern),

                SalesTransaction.store_name
                .ilike(search_pattern),

                SalesTransaction.country
                .ilike(search_pattern),

                SalesTransaction.region
                .ilike(search_pattern),

                SalesTransaction.city
                .ilike(search_pattern),

                SalesTransaction.product_id
                .ilike(search_pattern),

                SalesTransaction.product_name
                .ilike(search_pattern),

                SalesTransaction.product_category
                .ilike(search_pattern),

                SalesTransaction.product_subcategory
                .ilike(search_pattern),

                SalesTransaction.payment_method
                .ilike(search_pattern),

                SalesTransaction.order_status
                .ilike(search_pattern),

                SalesTransaction.shipping_method
                .ilike(search_pattern),

                SalesTransaction.return_flag
                .ilike(search_pattern),

                SalesTransaction.return_reason
                .ilike(search_pattern),

                SalesTransaction.sales_representative
                .ilike(search_pattern),

                SalesTransaction.promotion_code
                .ilike(search_pattern),

                SalesTransaction.storage_type
                .ilike(search_pattern),

                cast(
                    SalesTransaction.customer_age,
                    String
                ).ilike(search_pattern),

                cast(
                    SalesTransaction.quantity,
                    String
                ).ilike(search_pattern),

                cast(
                    SalesTransaction.unit_price,
                    String
                ).ilike(search_pattern),

                cast(
                    SalesTransaction.discount_percentage,
                    String
                ).ilike(search_pattern),

                cast(
                    SalesTransaction.sales_amount,
                    String
                ).ilike(search_pattern),

                cast(
                    SalesTransaction.cost_amount,
                    String
                ).ilike(search_pattern),

                cast(
                    SalesTransaction.profit,
                    String
                ).ilike(search_pattern),

                cast(
                    SalesTransaction.delivery_days,
                    String
                ).ilike(search_pattern),

                cast(
                    SalesTransaction.customer_rating,
                    String
                ).ilike(search_pattern),

                cast(
                    SalesTransaction.inventory_level,
                    String
                ).ilike(search_pattern),

                cast(
                    SalesTransaction.order_year,
                    String
                ).ilike(search_pattern),

                cast(
                    SalesTransaction.order_date,
                    String
                ).ilike(search_pattern),

                cast(
                    SalesTransaction.order_time,
                    String
                ).ilike(search_pattern)
            )
        )

    statement = (
        statement
        .order_by(
        SalesTransaction.transaction_id
        )
        .limit(safe_limit)
    )

    records = database.scalars(
        statement
    ).all()

    results = []

    for record in records:
        result = sql_record_to_dict(
            record
        )

        result["source"] = "SQL"

        results.append(
            result
        )

    return results


#------------------------------------------------
# MongoDB search
#------------------------------------------------

def search_mongodb(
    search_term: str = "",
    limit: int = DEFAULT_LIMIT
) -> list:
    safe_limit = normalize_limit(limit)

    cleaned_search_term = search_term.strip()

    mongo_query = {}

    # --------------------------------------------------------
    # Search when user has entered a search term
    # --------------------------------------------------------

    if cleaned_search_term:
        escaped_search_term = re.escape(
            cleaned_search_term
        )

        regex_query = {
            "$regex": escaped_search_term,
            "$options": "i"
        }

        # Text fields from the transaction document
        text_fields = [
            "transaction_id",
            "order_id",
            "customer_id",
            "customer_name",
            "customer_gender",
            "customer_segment",
            "order_date",
            "order_time",
            "sales_channel",
            "store_id",
            "store_name",
            "country",
            "region",
            "city",
            "product_id",
            "product_name",
            "product_category",
            "product_subcategory",
            "payment_method",
            "order_status",
            "shipping_method",
            "return_flag",
            "return_reason",
            "sales_representative",
            "promotion_code",
            "storage_type"
        ]

        search_conditions = []

        # Add text field searches
        for field in text_fields:
            search_conditions.append(
                {
                    field: regex_query
                }
            )

        # ----------------------------------------------------
        # Numeric search
        # ----------------------------------------------------

        try:
            numeric_value = float(
                cleaned_search_term
            )

            numeric_fields = [
                "unit_price",
                "discount_percentage",
                "sales_amount",
                "cost_amount",
                "profit",
                "customer_rating"
            ]

            for field in numeric_fields:
                search_conditions.append(
                    {
                        field: numeric_value
                    }
                )

            # Some values are integers rather than floats
            if numeric_value.is_integer():
                integer_value = int(
                    numeric_value
                )

                integer_fields = [
                    "customer_age",
                    "quantity",
                    "delivery_days",
                    "inventory_level",
                    "order_year",
                    "version"
                ]

                for field in integer_fields:
                    search_conditions.append(
                        {
                            field: integer_value
                        }
                    )

        except ValueError:
            # Search term is not a number.
            # Continue using text search only.
            pass

        mongo_query = {
            "$or": search_conditions
        }

    # --------------------------------------------------------
    # Execute MongoDB query
    # --------------------------------------------------------

    cursor = (
        mongo_collection
        .find(mongo_query)
        .sort(
            "transaction_id",
            1
        )
        .limit(safe_limit)
    )

    results = []

    # --------------------------------------------------------
    # Convert MongoDB documents for API response
    # --------------------------------------------------------

    for document in cursor:

        result = mongodb_document_to_dict(
            document
        )

        result["source"] = "NoSQL"

        results.append(
            result
        )

    return results



# ============================================================
# Combined search
# ============================================================

def search_all_databases(
    database: Session,
    search_term: str = "",
    limit: int = DEFAULT_LIMIT
) -> list:
    safe_limit = normalize_limit(
        limit
    )

    # Query enough records from both databases
    # so duplicate SHARED records can be merged.
    sql_results = search_postgresql(
        database=database,
        search_term=search_term,
        limit=MAX_LIMIT
    )

    mongodb_results = search_mongodb(
        search_term=search_term,
        limit=MAX_LIMIT
    )

    combined_records = {}

    # --------------------------------------------------------
    # Add PostgreSQL records
    # --------------------------------------------------------

    for record in sql_results:
        transaction_id = record[
            "transaction_id"
        ]

        combined_records[
            transaction_id
        ] = record

    # --------------------------------------------------------
    # Add MongoDB records
    # --------------------------------------------------------

    for mongo_record in mongodb_results:
        transaction_id = mongo_record[
            "transaction_id"
        ]

        if transaction_id in combined_records:
            sql_record = combined_records[
                transaction_id
            ]

            # The transaction exists in both databases.
            sql_record["source"] = (
                "SQL + NoSQL"
            )

            sql_record["sql_version"] = (
                sql_record.get("version")
            )

            sql_record["nosql_version"] = (
                mongo_record.get("version")
            )

            if (
            sql_record.get("version")
                == mongo_record.get("version")
            ):
                sql_record[
                "replication_status"
                ] = "SYNCED"

            else:
                sql_record[
                    "replication_status"
                ] = "VERSION_MISMATCH"

        else:
            # MongoDB-only transaction.
            combined_records[
                transaction_id
            ] = mongo_record

    # --------------------------------------------------------
    # Sort results
    # --------------------------------------------------------

    sorted_records = sorted(
        combined_records.values(),
        key=lambda record:
            record["transaction_id"]
    )

    return sorted_records[
        :safe_limit
    ]



# ============================================================
# Generic source selector
# ============================================================

def search_records(
    source: str,
    database: Session,
    search_term: str = "",
    limit: int = DEFAULT_LIMIT
) -> list:
    normalized_source = (
        source
        .strip()
        .lower()
    )

    if normalized_source == "sql":
        return search_postgresql(
            database=database,
            search_term=search_term,
            limit=limit
        )

    if normalized_source in {
        "nosql",
        "mongodb",
        "mongo"
    }:
        return search_mongodb(
            search_term=search_term,
            limit=limit
        )

    if normalized_source in {
        "all",
        "both"
    }:
        return search_all_databases(
            database=database,
            search_term=search_term,
            limit=limit
        )

    raise ValueError(
        "Unknown search source. "
        "Expected one of: "
        "all, sql, nosql."
    )
