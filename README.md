# SQL and NoSQL Data Management System

This project is a full-stack application that uses both a relational SQL database and a NoSQL document database.

The application was developed as a Data-Intensive Systems course assignment. The purpose of the project is to demonstrate data partitioning between PostgreSQL and MongoDB, searching across both databases, modifying data, and synchronizing replicated records.

## Technologies

### Backend

- Python
- FastAPI
- SQLAlchemy
- Psycopg
- PyMongo
- Pydantic

### Databases

- PostgreSQL
- MongoDB

### Frontend

- React
- Vite
- JavaScript
- CSS

### Development Tools

- Visual Studio Code
- pgAdmin 4
- MongoDB Compass
- Git
- GitHub

---

## Dataset

The provided CSV file contains a data dictionary describing the structure of sales transaction data.

Because the provided file contains schema definitions rather than actual transaction records, a synthetic dataset was generated based on the provided:

- column names
- data types
- example values
- business meanings

The data generator is located at:

```text
data/generate_mock_data.py
```

The generator uses a fixed random seed so that the same dataset is created every time.

It generates:

```text
300 synthetic sales transactions
```

The generated dataset is stored in:

```text
data/sales_mock_data.csv
```

---

## Data Partitioning

The 300 unique transactions are divided into three equal groups.

```text
100 SQL_ONLY
100 NOSQL_ONLY
100 SHARED
```

### SQL_ONLY

100 transactions exist only in PostgreSQL.

### NOSQL_ONLY

100 transactions exist only in MongoDB.

### SHARED

100 transactions are replicated into both PostgreSQL and MongoDB.

Therefore the physical record counts are:

```text
PostgreSQL:
100 SQL_ONLY
+ 100 SHARED
= 200 records

MongoDB:
100 NOSQL_ONLY
+ 100 SHARED
= 200 documents
```

The total number of unique transactions remains:

```text
300
```

---

## Architecture

```text
            React + Vite
                |
                | HTTP / JSON
                v
             FastAPI
                |
    +-----------+-----------+
    |                       |
    v                       v
SQLAlchemy              PyMongo
    |                       |
    v                       v
PostgreSQL              MongoDB
sales_sql_db        sales_nosql_db
    |                       |
    +-----------+-----------+
                |
            SHARED data
```

FastAPI provides a common application layer for accessing both database technologies.

---

## PostgreSQL

The SQL database is:

```text
sales_sql_db
```

The primary table is:

```text
sales_transactions
```

The SQL database contains:

```text
SQL_ONLY
SHARED
```

transactions.

---

## MongoDB

The MongoDB database is:

```text
sales_nosql_db
```

The collection is:

```text
sales_transactions
```

The NoSQL database contains:

```text
NOSQL_ONLY
SHARED
```

transactions.

---

## Search Functionality

The backend supports searches against each database individually and across both databases.

Available search sources are:

```text
sql
nosql
all
```

Example endpoints:

```text
GET /api/search/sql?q=Laptop
GET /api/search/nosql?q=Laptop
GET /api/search/all?q=Laptop
```

The search supports text and numeric fields.

Example search terms include:

```text
Laptop
Helsinki
Completed
2024
899
SHARED
```

### Combined Search

When searching all databases, SHARED transactions would normally appear twice because they exist in both PostgreSQL and MongoDB.

The application deduplicates combined results using:

```text
transaction_id
```

Therefore a complete unfiltered search produces:

```text
PostgreSQL: 200 records
MongoDB: 200 records
All Data: 300 unique records
```

---

## Data Modification

Transactions can be modified through the FastAPI backend.

The update endpoint is:

```text
PATCH /api/transactions/{transaction_id}
```

Partial updates are supported.

Example:

```json
{
"customer_rating": 5
}
```

Certain system-managed fields cannot be modified manually:

```text
transaction_id
storage_type
version
```

---

## Replication Protocol

The system implements synchronous application-level replication for SHARED records.

The update behavior depends on the location of the transaction.

```text
SQL_ONLY
|
v
PostgreSQL


NOSQL_ONLY
|
v
MongoDB


SHARED
|
v
PostgreSQL + MongoDB
```

Each transaction contains a version number.

Example initial state:

```text
PostgreSQL version = 1
MongoDB version = 1
```

After modifying a SHARED record:

```text
PostgreSQL version = 2
MongoDB version = 2
```

The replication result is reported as:

```text
SYNCED
```

when both versions match.

If the versions differ, the replication layer reports:

```text
VERSION_MISMATCH
```

The replication implementation also includes rollback or compensation handling for database update failures.

---

## Example Replication

A SHARED transaction such as:

```text
T20000201
```

can exist simultaneously in PostgreSQL and MongoDB.

Updating:

```json
{
"customer_rating": 5
}
```

updates both database copies and increases the version number.

The application can then verify:

```text
PostgreSQL:
customer_rating = 5
version = 2

MongoDB:
customer_rating = 5
version = 2

Replication status:
SYNCED
```

---

# Project Structure

```text
data_intensive_A4/
|
├── data/
│ ├── sales_data_dictionary.csv
│ ├── sales_mock_data.csv
│ └── generate_mock_data.py
|
├── backend/
│ ├── .env.example
│ ├── requirements.txt
│ ├── create_tables.py
│ ├── import_data.py
│ ├── test_connection.py
│ |
│ └── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── search.py
│   ├── replication.py
│   └── main.py
|
├── frontend/
│ ├── package.json
│ ├── package-lock.json
│ ├── vite.config.js
│ |
│ └── src/
│    ├── api.js
│    ├── App.jsx
│    ├── index.css
│    └── main.jsx
|
├── .gitignore
└── README.md
```

---

# Installation

## Requirements

Install the following software:

- Python
- PostgreSQL
- MongoDB Community Server
- Node.js and npm
- Git

The databases can be inspected using:

- pgAdmin 4
- MongoDB Compass

---

## 1. Create the PostgreSQL Database

Create:

```sql
CREATE DATABASE sales_sql_db;
```

MongoDB does not need to be created manually. The MongoDB database and collection are created when documents are first inserted.

---

## 2. Backend Setup

Navigate to:

```text
backend/
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

---

## 3. Environment Configuration

Create:

```text
backend/.env
```

using:

```text
backend/.env.example
```

as a template.

Example:

```env
SQL_DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/sales_sql_db
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=sales_nosql_db
```

Replace:

```text
YOUR_PASSWORD
```

with the local PostgreSQL password.

The real `.env` file is excluded from Git.

---

## 4. Generate Synthetic Data

From the project backend directory, run:

```powershell
python ..\data\generate_mock_data.py
```

The generator validates that the resulting dataset contains:

```text
Total records: 300
SQL_ONLY: 100
NOSQL_ONLY: 100
SHARED: 100
```

---

## 5. Create PostgreSQL Tables

Run:

```powershell
python create_tables.py
```

This creates:

```text
sales_transactions
```

inside:

```text
sales_sql_db
```

---

## 6. Import Data

Run:

```powershell
python import_data.py
```

The importer distributes records according to `storage_type`.

Expected result:

```text
PostgreSQL: 200
MongoDB: 200
```

---

## 7. Start Backend

Run:

```powershell
uvicorn app.main:app --reload
```

FastAPI runs at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

## 8. Start Frontend

Open another terminal:

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

Start Vite:

```powershell
npm run dev
```

If PowerShell blocks the npm PowerShell wrapper, use:

```powershell
npm.cmd run dev
```

The Vite terminal displays the local frontend address.

---


# Security

Sensitive environment variables are stored in:

```text
backend/.env
```

and excluded using `.gitignore`.

The repository should not contain:

```text
backend/.env
backend/.venv/
frontend/node_modules/
frontend/dist/
```

---

# Author

joonasaf

Data-Intensive Systems Course Project
