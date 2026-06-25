# Address Book API

A RESTful Address Book application built with FastAPI and SQLite.

## Features

- Create an address
- Retrieve all addresses
- Retrieve an address by ID
- Update an address
- Delete an address
- Search nearby addresses using latitude, longitude, and radius
- Automatic validation using Pydantic
- Interactive Swagger documentation

## Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

## Installation

```bash
git clone https://github.com/TrojanFly21/address-book-api.git

cd address-book-api

python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the server:

```bash
cd address-book-api

uvicorn app.main:app --reload
```

## Swagger UI

```
http://127.0.0.1:8000/docs
```

## Example Nearby Search

```
GET /addresses/search/nearby?latitude=12.9716&longitude=77.5946&radius_km=2
```

## Run Tests

```bash
cd address-book-api

python -m pytest tests/test_address.py -vs
```
