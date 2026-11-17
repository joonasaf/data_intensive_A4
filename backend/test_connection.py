from sqlalchemy import text

from app.database import(
    mongo_client,
    sql_engine
)

def test_postgresql():
    print("Testing PostgreSQL...")

    try:
        with sql_engine.connect() as connection:
            result = connection.execute(
                text("SELECT current_database();")
            )

            database_name = result.scalar()

            print(
                f"PostgreSQL conncetion successful: "
                f"{database_name}"
            )

    except Exception as error:
        print(
            f"PostgreSQL connection failed: "
            f"{error}"
        )

def test_mongodb():
    print("Testing MongoDB...")

    try:
        result = mongo_client.admin.command(
            "ping"
        )

        if result.get("ok") == 1.0:
            print("MongoDB connection successful.")
        else:
            print("MongoDB responded, but ping was not successful.")

    except Exception as error:
        print(
            f"MongoDB conncetion failed: "
            f"{error}"
        )

def main():
    print("Database connection test")
    print("------------------------")

    test_postgresql()

    print()

    test_mongodb()

if __name__ == "__main__":
    main()