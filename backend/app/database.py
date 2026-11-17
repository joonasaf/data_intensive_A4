from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

# -------------------------------------------
# PostgreSQL
# -------------------------------------------

sql_engine = create_engine(
    settings.sql_database_url,
    pool_pre_ping=True
)

SqlSessionLocal = sessionmaker(
    bind=sql_engine,
    autoflush=False,
    autocommit=False
)

class SqlBase(DeclarativeBase):
    pass

def get_sql_db():
    database = SqlSessionLocal()

    try:
        yield database
    finally:
        database.close()


# -------------------------------------------
# MongoDB
# -------------------------------------------

mongo_client = MongoClient(
    settings.mongodb_url
)

mongo_database = mongo_client[
    settings.mongodb_database
]

mongo_collection = mongo_database[
    "sales_transactions"
]