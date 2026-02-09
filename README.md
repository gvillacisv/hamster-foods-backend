# Backend API

This is the FastAPI backend for the Hamster Foods Tier Status application.

## Setup

1.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```

2.  **Activate the virtual environment:**
    - On macOS/Linux: `source .venv/bin/activate`
    - On Windows: `.\.venv\Scripts\activate`

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the database:**
    This command will create `hamster_foods.db` and populate it with schema and seed data. Run this once during setup.
    ```bash
    python initialize_db.py
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

## Architecture Decision Records (ADRs)

This project uses Architecture Decision Records to document important architectural choices.

- [ADR 1: Single Source of Truth](./docs/adr-001-single-source-of-truth.md)
- [ADR 2: Pessimistic Locking for Concurrency Control](./docs/adr-002-pessimistic-locking.md)
- [ADR 3: Currency Stability](./docs/adr-003-currency-stability.md)
- [ADR 4: History-Based State Persistence](./docs/adr-004-history-based-state.md)
