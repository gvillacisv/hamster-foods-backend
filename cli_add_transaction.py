import sqlite3
import os
import uuid
from datetime import datetime
import requests
from InquirerPy import inquirer
from InquirerPy.validator import NumberValidator

API_BASE_URL = "http://localhost:8000/api/v1"
DB_FILE = os.path.join(os.path.dirname(__file__), '.', 'hamster_foods.db')

RATES_TO_BASE = {
    "EUR": 1.0,
    "GBP": 1.18,
    "USD": 0.93,
}
SUPPORTED_CURRENCIES = list(RATES_TO_BASE.keys())

def get_db_connection():
    try:
        connection = sqlite3.connect(DB_FILE)
        connection.row_factory = sqlite3.Row

        return connection
    except sqlite3.Error as exception:
        print(f"\n[ERROR] Could not connect to the database at '{DB_FILE}'.")
        print("Please ensure the path is correct and the database has been initialized.")
        print(f"Details: {exception}")

        return None

def get_existing_customers():
    connection = get_db_connection()
    if not connection: return []

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, name FROM customers ORDER BY name")
        customers = cursor.fetchall()

        return [{"name": f"{row['name']} ({row['id']})", "value": row['id']} for row in customers]
    finally:
        if connection: connection.close()

def create_new_customer(name: str) -> str:
    connection = get_db_connection()

    if not connection: return ""

    customer_id = f"customer-{uuid.uuid4().hex[:8]}"

    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO customers (id, name) VALUES (?, ?)", (customer_id, name))
        connection.commit()

        return customer_id
    finally:
        if connection: connection.close()

def add_order_for_customer(customer_id, amount, currency, amount_base, rate) -> str:
    connection = get_db_connection()

    if not connection: return ""

    order_id = f"order-{uuid.uuid4().hex[:10]}"

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO orders (id, customer_id, amount_value, amount_currency, amount_base, exchange_rate, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (order_id, customer_id, amount, currency, amount_base, rate, datetime.now().isoformat())
        )
        connection.commit()

        return order_id
    finally:
        if connection: connection.close()

def sync_customer_tier(customer_id: str, order_id: str):
    print(f"\nAttempting to sync tier for customer {customer_id} via API...")
    endpoint = f"{API_BASE_URL}/customers/{customer_id}/sync-tier"
    payload = {"reason": "TRANSACTION", "orderId": order_id}

    try:
        response = requests.post(endpoint, json=payload, timeout=10)
        response.raise_for_status()
        print(f"✅ Tier sync successful! Check the frontend for updates.")

        return True
    except requests.exceptions.RequestException as e:
        print(f"\n[ERROR] Failed to sync tier for customer {customer_id}.")
        print("Please ensure the backend API server is running on http://localhost:8000.")
        print(f"Details: {e}")

        return False

def handle_existing_customer():
    customers = get_existing_customers()

    if not customers:
        print("\nCould not find any customers in the database.")

        return

    choices = [{"name": "<-- Go Back", "value": "back"}] + customers

    customer_id = inquirer.select(
        message="Select a customer:",
        choices=choices,
        vi_mode=True
    ).execute()
    
    if customer_id == "back":
        return

    if customer_id:
        process_transaction_details(customer_id)

def handle_new_customer():
    customer_name = inquirer.text(
        message="Enter the new customer's name (or leave blank to go back):",
    ).execute()

    if not customer_name:
        print("\nCancelled creating new customer.")

        return

    customer_id = create_new_customer(customer_name)

    if customer_id:
        print(f"\nCustomer '{customer_name}' created with ID: {customer_id}")
        process_transaction_details(customer_id)
    else:
        print(f"\nFailed to create customer '{customer_name}'.")

def process_transaction_details(customer_id):
    print(f"\nAdding a new transaction for customer ID: {customer_id}")
    amount_str = inquirer.text(
        message="Enter transaction amount:",
        validate=NumberValidator(float_allowed=True, message="Please enter a valid number."),
    ).execute()
    amount = float(amount_str)

    currency = inquirer.select(
        message="Select currency:",
        choices=SUPPORTED_CURRENCIES,
    ).execute().upper()

    rate = RATES_TO_BASE[currency]
    amount_base = round(amount * rate, 2)

    print(f"\nTransaction Summary:")
    print(f"  - Amount: {amount:.2f} {currency}")
    print(f"  - Rate (to EUR): {rate}")
    print(f"  - Value in EUR: {amount_base:.2f}")

    confirm = inquirer.confirm(message="Proceed to add this transaction?", default=True).execute()

    if confirm:
        order_id = add_order_for_customer(customer_id, amount, currency, amount_base, rate)

        if order_id:
            print(f"\n✅ Transaction of {amount:.2f} {currency} added successfully (Order ID: {order_id}).")
            sync_customer_tier(customer_id, order_id)
    else:
        print("\nTransaction cancelled.")

def main():
    print("--- Hamster Foods Transaction CLI ---\n")

    while True:
        action = inquirer.select(
            message="What would you like to do?",
            choices=[
                {"name": "Add a transaction for an EXISTING customer", "value": "existing"},
                {"name": "Create a NEW customer and add their first transaction", "value": "new"},
                {"name": "Exit", "value": "exit"}
            ],
            default="existing"
        ).execute()

        if action == "existing":
            handle_existing_customer()
        elif action == "new":
            handle_new_customer()
        elif action == "exit":
            break

    print("\nExiting CLI. Goodbye!")

if __name__ == "__main__":
    main()
