# FastAPI Tier Status Backend

This is a demo/portfolio project showcasing a FastAPI backend implementing a tier status and loyalty system. Built with assistance from Agentic AI for learning and demonstration purposes.

## Quick Start

```bash
# Clone and setup (one-liner)
python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && cp .env.example .env && python initialize_db.py

# Run tests
pytest

# Start server
uvicorn main:app --reload
```

## Purpose

This project demonstrates:
- FastAPI REST API development
- SQLite database with tier status tracking
- Currency exchange and rolling window calculations
- Interactive CLI tool for database manipulation

## Setup

1. **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

2. **Activate the virtual environment:**
    - On macOS/Linux: `source venv/bin/activate`
    - On Windows: `.\venv\Scripts\activate`

3. **Install dependencies:**
    For a production-only environment, use `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure environment variables:**
    Copy `.env.example` to `.env` and configure:
    ```bash
    cp .env.example .env
    ```
    
    Key configuration options:
    - `DATABASE_URL` - Path to SQLite database (default: `tier_status.db`)
    - `API_KEY` - Set to enable API key authentication (leave empty for dev mode)
    - `CORS_ORIGINS` - Comma-separated list of allowed origins (e.g., `http://localhost:3000`)
    - `DEBUG` - Set to `true` for debug mode

5. **Initialize the database:**
    This command will create `tier_status.db` and populate it with schema and seed data. Run this once during setup.
    ```bash
    python initialize_db.py
    ```

## Test

1. **Install dependencies:**
    For a development environment, use `requirements-dev.txt`:
    ```bash
    pip install -r requirements-dev.txt
    ```

2. **Run tests:**
    ```bash
    pytest
    ```

3. **Run tests with coverage:**
    ```bash
    pytest --cov=api --cov-report=term-missing
    ```

## Reset the Database

To recreate the database from scratch:
```bash
rm tier_status.db 2>/dev/null
python initialize_db.py
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Ensure venv is activated: `source venv/bin/activate` |
| `No module named pytest` | Install dev deps: `pip install -r requirements-dev.txt` |
| Port 8000 in use | Kill process: `lsof -ti:8000 \| xargs kill` or use `uvicorn --port 8001` |
| Database locked | Delete `.db-journal` files: `rm *.db-journal` |

## Running the API

To run the API in development mode with auto-reload (on active virtual environment):
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.
For observability, the Health Check endpoint will be available at `http://localhost:8000/health`.
You can access the auto-generated documentation at `http://localhost:8000/docs`.

## API Endpoints

The API provides the following endpoints under the `/api/v1` prefix. For detailed information and to interact with the API, run the server and visit `http://localhost:8000/docs`.

### Tiers

- `GET /customers/{customer_id}/tier-status`: Get customer's current tier status.
- `POST /customers/{customer_id}/sync-tier`: Trigger a manual tier synchronization for a customer.

# CLI Tool: Add Transaction

This script provides an interactive command-line interface to add new transactions to the database for testing and demonstration purposes.

It supports:
- Creating a brand new customer and adding their first transaction.
- Selecting an existing customer from a list and adding a new transaction for them.

Run script:
```bash
python cli_add_transaction.py
```

## Documentation

This project uses Architecture Decision Records (ADR) and Request for Comments (RFC) to document important architectural choices.

### ADRs
- [ADR 001: Rolling Window](./docs/adr-001-rolling-window.md)
- [ADR 002: Single Source of Truth](./docs/adr-002-single-source-of-truth.md)
- [ADR 003: Pessimistic Locking for Concurrency Control](./docs/adr-003-pessimistic-locking.md)
- [ADR 004: Currency Stability](./docs/adr-004-currency-stability.md)
- [ADR 005: History-Based State Persistence](./docs/adr-005-history-based-state.md)

### RFCs
- [RFC 001: Unified Currency and Tiering Service Integration](./docs/rfc-001-tiering-and-currency-logic.md)
