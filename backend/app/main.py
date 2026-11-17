from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
)

from sqlalchemy.orm import Session
from app.database import get_sql_db
from app.search import search_records
from app import schemas
from app.replication import (
    InvalidUpdateError,
    RecordNotFoundError,
    ReplicationError,
    update_transaction
)

app = FastAPI(
    title="SQL and NoSQL Management API",
    version="1.0.0"
)

#---------------------------------------------
# Health Check
#---------------------------------------------

@app.get("/api/health")
def health_check():
    return{
        "status": "ok"
    }


#---------------------------------------------
# Search
#---------------------------------------------

@app.get("/api/search/{source}")
def search_data(
    source: str,
    q: str = "",
    limit: int = 100,
    database: Session = Depends(get_sql_db)
):
    try:
        return search_records(
            source=source,
            database=database,
            search_term=q,
            limit=limit
        )
    
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


#---------------------------------------------
# Update
#---------------------------------------------

@app.patch("/api/transactions/{transaction_id}")
def update_transaction_record(
    transaction_id: str,
    update_data: schemas.SalesTransactionUpdate,
    database: Session = Depends(get_sql_db)
):
    updates = update_data.model_dump(
        exclude_none=True
    )

    try:
        return update_transaction(
            database=database,
            transaction_id=transaction_id,
            updates=updates
        )


    except RecordNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        ) from error

    except InvalidUpdateError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        ) from error


    except ReplicationError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        ) from error

