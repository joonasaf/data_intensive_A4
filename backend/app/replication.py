from copy import deepcopy
from datetime import date, datetime, time
from decimal import Decimal


from pymongo.errors import PyMongoError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


from app.database import mongo_collection
from app.models import SalesTransaction




#------------------------------------------------
# Configuration
#------------------------------------------------


STORAGE_SQL_ONLY = "SQL_ONLY"
STORAGE_NOSQL_ONLY = "NOSQL_ONLY"
STORAGE_SHARED = "SHARED"




IMMUTABLE_FIELDS = {
    "transaction_id",
    "storage_type",
    "version",
    "_id"
}




EDITABLE_FIELDS = {
    "order_id",
    "customer_id",
    "customer_name",
    "customer_age",
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
    "quantity",
    "unit_price",
    "discount_percentage",
    "sales_amount",
    "cost_amount",
    "profit",
    "payment_method",
    "order_status",
    "shipping_method",
    "delivery_days",
    "return_flag",
    "return_reason",
    "sales_representative",
    "promotion_code",
    "customer_rating",
    "inventory_level",
    "order_year"
}




#------------------------------------------------
# Exceptions
#------------------------------------------------


class ReplicationError(Exception):
    pass




class RecordNotFoundError(Exception):
    pass




class InvalidUpdateError(Exception):
    pass




#------------------------------------------------
# Value conversion
#------------------------------------------------


def convert_value_for_mongodb(value):
    """
    Convert Python and SQLAlchemy-compatible values into values
    that can be stored safely in MongoDB.
    """


    if isinstance(value, Decimal):
        return float(value)


    if isinstance(value, datetime):
        return value.isoformat()


    if isinstance(value, date):
        return value.isoformat()


    if isinstance(value, time):
        return value.isoformat()


    return value




def convert_updates_for_mongodb(updates):
    return {
        field: convert_value_for_mongodb(value)
        for field, value in updates.items()
    }




#------------------------------------------------
# Validation
#------------------------------------------------


def validate_updates(updates):
    if not isinstance(updates, dict):
        raise InvalidUpdateError(
            "Update data must be a dictionary."
    )


    if not updates:
        raise InvalidUpdateError(
            "No fields were provided for the update."
    )


    unknown_fields = (
        set(updates.keys())
        - EDITABLE_FIELDS
        - IMMUTABLE_FIELDS
    )


    if unknown_fields:
        field_list = ", ".join(
            sorted(unknown_fields)
        )


        raise InvalidUpdateError(
            f"Unknown update fields: {field_list}"
        )


    immutable_updates = (
        set(updates.keys())
        & IMMUTABLE_FIELDS
    )


    if immutable_updates:
        field_list = ", ".join(
            sorted(immutable_updates)
        )


        raise InvalidUpdateError(
            "The following fields cannot be modified: "
            f"{field_list}"
        )


    return {
        field: value
        for field, value in updates.items()
        if field in EDITABLE_FIELDS
    }




#------------------------------------------------
# Record lookup
#------------------------------------------------


def get_sql_record(
    database: Session,
    transaction_id: str
):
    return database.get(
        SalesTransaction,
        transaction_id
    )




def get_mongodb_record(
    transaction_id: str
):
    return mongo_collection.find_one({
        "transaction_id": transaction_id
    })




def determine_storage_type(
    sql_record,
    mongodb_record
):
    if (
        sql_record is not None
        and mongodb_record is not None
    ):
        return STORAGE_SHARED


    if sql_record is not None:
        return STORAGE_SQL_ONLY


    if mongodb_record is not None:
        return STORAGE_NOSQL_ONLY


    raise RecordNotFoundError(
        "Transaction was not found in PostgreSQL or MongoDB."
    )




#------------------------------------------------
# PostgreSQL update
#------------------------------------------------


def apply_sql_updates(
    sql_record,
    updates,
    new_version
):
    for field, value in updates.items():
        setattr(
            sql_record,
            field,
            value
        )


    sql_record.version = new_version




def update_sql_only(
    database: Session,
    sql_record,
    updates
):
    current_version = int(
        sql_record.version
    )


    new_version = (
        current_version + 1
    )


    apply_sql_updates(
        sql_record=sql_record,
        updates=updates,
        new_version=new_version
    )


    try:
        database.commit()
        database.refresh(sql_record)


    except SQLAlchemyError as error:
        database.rollback()


        raise ReplicationError(
            "PostgreSQL update failed."
        ) from error


    return {
        "transaction_id":
            sql_record.transaction_id,


        "storage_type":
            STORAGE_SQL_ONLY,


        "version":
            sql_record.version,


        "replication_status":
            "NOT_REQUIRED",


        "updated_databases": [
            "PostgreSQL"
        ]
    }




#------------------------------------------------
# MongoDB update
#------------------------------------------------


def update_nosql_only(
    mongodb_record,
    updates
):
    current_version = int(
        mongodb_record.get(
            "version",
            1
        )
    )


    new_version = (
        current_version + 1
    )


    mongodb_updates = (
        convert_updates_for_mongodb(
            updates
        )
    )


    mongodb_updates["version"] = (
        new_version
    )


    try:
        result = mongo_collection.update_one(
            {
                "transaction_id":
                    mongodb_record[
                        "transaction_id"
                    ],


                "version":
                    current_version
            },
            {
                "$set":
                    mongodb_updates
            }
        )


    except PyMongoError as error:
        raise ReplicationError(
            "MongoDB update failed."
        ) from error


    if result.matched_count != 1:
        raise ReplicationError(
            "MongoDB record was changed by another "
            "operation or could not be found."
    )


    updated_record = (
        get_mongodb_record(
            mongodb_record[
                "transaction_id"
            ]
        )
    )


    if updated_record is None:
        raise ReplicationError(
            "Updated MongoDB record could not be verified."
        )


    return {
        "transaction_id":
            mongodb_record[
                "transaction_id"
            ],


        "storage_type":
            STORAGE_NOSQL_ONLY,


        "version":
            updated_record.get(
                "version"
            ),


        "replication_status":
            "NOT_REQUIRED",


        "updated_databases": [
            "MongoDB"
        ]
    }




#------------------------------------------------
# Shared synchronous replication
#------------------------------------------------


def restore_mongodb_record(
    original_document
):
    if original_document is None:
        return


    document_to_restore = deepcopy(
        original_document
    )


    mongo_id = document_to_restore.pop(
        "_id",
        None
    )


    if mongo_id is not None:
        mongo_collection.replace_one(
            {
                "_id": mongo_id
            },
            document_to_restore,
            upsert=True
        )


        return


    mongo_collection.replace_one(
        {
            "transaction_id":
                document_to_restore[
                    "transaction_id"
                ]
        },
        document_to_restore,
        upsert=True
    )




def update_shared_record(
    database: Session,
    sql_record,
    mongodb_record,
    updates
):
    sql_version = int(
        sql_record.version
    )


    mongodb_version = int(
        mongodb_record.get(
            "version",
            1
        )
    )


    if sql_version != mongodb_version:
        raise ReplicationError(
            "Replication cannot continue because "
            "PostgreSQL and MongoDB versions differ. "
            f"PostgreSQL version: {sql_version}. "
            f"MongoDB version: {mongodb_version}."
        )


    new_version = (
        sql_version + 1
    )


    original_mongodb_record = deepcopy(
        mongodb_record
    )


    mongodb_updates = (
        convert_updates_for_mongodb(
            updates
        )
    )


    mongodb_updates["version"] = (
        new_version
    )


    # Apply changes to the SQLAlchemy object, but do not
    # commit PostgreSQL yet.
    apply_sql_updates(
        sql_record=sql_record,
        updates=updates,
        new_version=new_version
    )


    try:
        mongo_result = (
            mongo_collection.update_one(
                {
                    "transaction_id":
                    sql_record.transaction_id,

                    "version":
                    mongodb_version
                },
                {
                    "$set":
                    mongodb_updates
                }
            )
        )


        if mongo_result.matched_count != 1:
            database.rollback()


            raise ReplicationError(
                "MongoDB shared record was changed "
                "by another operation or could not "
                "be found."
            )


        # Commit PostgreSQL only after MongoDB update succeeds.
        database.commit()
        database.refresh(
            sql_record
        )


    except PyMongoError as error:
        database.rollback()


        raise ReplicationError(
            "MongoDB replication failed. "
            "PostgreSQL was rolled back."
        ) from error


    except SQLAlchemyError as error:
        database.rollback()


        # MongoDB is not part of the PostgreSQL transaction.
        # Restore its previous state when SQL commit fails.
        try:
            restore_mongodb_record(
                original_mongodb_record
            )
        except PyMongoError as restore_error:
            raise ReplicationError(
                "PostgreSQL commit failed and MongoDB "
                "compensation also failed. Manual "
                "reconciliation is required."
            ) from restore_error


        raise ReplicationError(
            "PostgreSQL commit failed. MongoDB was "
            "restored to its previous state."
        ) from error


    # Verify both database copies after the update.
    verified_mongodb_record = (
        get_mongodb_record(
            sql_record.transaction_id
        )
    )


    if verified_mongodb_record is None:
        raise ReplicationError(
            "MongoDB replication could not be verified."
        )


    verified_sql_version = int(
        sql_record.version
    )


    verified_mongodb_version = int(
        verified_mongodb_record.get(
            "version",
            0
        )
    )


    replication_status = (
        "SYNCED"
        if (
            verified_sql_version
            == verified_mongodb_version
        )
        else "VERSION_MISMATCH"
    )


    if replication_status != "SYNCED":
        raise ReplicationError(
            "Shared record update completed, but "
            "replication versions do not match."
        )


    return {
        "transaction_id":
            sql_record.transaction_id,


        "storage_type":
            STORAGE_SHARED,


        "version":
            verified_sql_version,


        "sql_version":
            verified_sql_version,


        "nosql_version":
            verified_mongodb_version,


        "replication_status":
            replication_status,


        "updated_databases": [
            "PostgreSQL",
            "MongoDB"
        ]
    }




#------------------------------------------------
# Public update entry point
#------------------------------------------------


def update_transaction(
    database: Session,
    transaction_id: str,
    updates: dict
):
    cleaned_transaction_id = (
        transaction_id.strip()
    )


    if not cleaned_transaction_id:
        raise InvalidUpdateError(
            "Transaction ID cannot be empty."
        )


    validated_updates = (
        validate_updates(
            updates
        )
    )


    sql_record = get_sql_record(
        database=database,
        transaction_id=cleaned_transaction_id
    )


    mongodb_record = get_mongodb_record(
        transaction_id=cleaned_transaction_id
    )


    storage_type = determine_storage_type(
        sql_record=sql_record,
        mongodb_record=mongodb_record
    )


    if storage_type == STORAGE_SQL_ONLY:
        return update_sql_only(
            database=database,
            sql_record=sql_record,
            updates=validated_updates
        )


    if storage_type == STORAGE_NOSQL_ONLY:
        return update_nosql_only(
            mongodb_record=mongodb_record,
            updates=validated_updates
        )


    if storage_type == STORAGE_SHARED:
        return update_shared_record(
            database=database,
            sql_record=sql_record,
            mongodb_record=mongodb_record,
            updates=validated_updates
        )


    raise ReplicationError(
        "Unsupported storage type."
    )
