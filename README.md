# Backend API

This is the FastAPI backend for the Hamster Foods Tier Status application.

## Setup

1.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

2.  **Activate the virtual environment:**
    - On macOS/Linux: `source venv/bin/activate`
    - On Windows: `.\venv\Scripts\activate`

3.  **Install dependencies:**
    For a production-only environment, use `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the database:**
    This command will create `hamster_foods.db` and populate it with schema and seed data. Run this once during setup.
    ```bash
    python initialize_db.py
    ```

## Test

1.  **Install dependencies:**
    For a development environment, use `requirements-dev.txt`:
    ```bash
    pip install -r requirements-dev.txt
    ```

2.  **Run tests*:*
    ```bash
    pytest
    ```

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