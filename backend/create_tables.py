from app.database import SqlBase, sql_engine

from app import models

def create_tables():
    print("Crreating PostgreSQL tables...")

    SqlBase.metadata.create_all(
        bind=sql_engine
    )

    print("PostgreSQL tables created successfully.")

if __name__ == "__main__":
    create_tables()