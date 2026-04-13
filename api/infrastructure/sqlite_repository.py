import sqlite3
from datetime import datetime
from typing import Optional, List

from api.application.ports import CustomerRepository
from api.domain.constants import Tier
from api.domain.models import Customer, Order, TierHistoryItem
from api.infrastructure.config import get_database_url


def get_db_connection():
    db_path = get_database_url()
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row

    return connection

class SqliteCustomerRepository(CustomerRepository):

    def get_customer_by_id(self, customer_id: str) -> Optional[Customer]:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, name FROM customers WHERE id = ?", (customer_id,))
            row = cursor.fetchone()

            if row:
                return Customer(id=row['id'], name=row['name'])

            return None

    def get_orders_for_customer_since(self, customer_id: str, date_from: datetime) -> List[Order]:
        orders = []

        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, customer_id, amount_value, amount_currency, amount_base, exchange_rate, created_at
                FROM orders
                WHERE customer_id = ? AND created_at >= ?
                """,
                (customer_id, date_from.strftime('%Y-%m-%d %H:%M:%S'))
            )

            rows = cursor.fetchall()

            for row in rows:
                orders.append(Order(
                    id=row['id'],
                    customer_id=row['customer_id'],
                    amount_value=row['amount_value'],
                    amount_currency=row['amount_currency'],
                    amount_base=row['amount_base'],
                    exchange_rate=row['exchange_rate'],
                    created_at=datetime.fromisoformat(row['created_at'])
                ))

        return orders

    def get_tier_history_desc(self, customer_id: str) -> List[TierHistoryItem]:
        history = []

        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, tier, date, total_base_at_change, change_reason
                FROM tier_history
                WHERE customer_id = ?
                ORDER BY date DESC
                """,
                (customer_id,)
            )

            rows = cursor.fetchall()

            for row in rows:
                history.append(TierHistoryItem(
                    id=row['id'],
                    tier=Tier(row['tier']),
                    date=datetime.fromisoformat(row['date']),
                    total_base_at_change=row['total_base_at_change'],
                    change_reason=row['change_reason']
                ))

        return history

    def get_current_tier(self, customer_id: str) -> tuple[Tier, float]:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT tier, total_base_at_change FROM tier_history WHERE customer_id = ? ORDER BY date DESC LIMIT 1",
                (customer_id,)
            )

            row = cursor.fetchone()

            if row:
                return Tier(row['tier']), row['total_base_at_change']

            return Tier.NO_TIER, -1.0

    def get_order_total_since(self, customer_id: str, date_from: datetime) -> float:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT SUM(amount_base) as total FROM orders WHERE customer_id = ? AND created_at >= ?",
                (customer_id, date_from.strftime('%Y-%m-%d %H:%M:%S'))
            )

            row = cursor.fetchone()

            if row and row['total'] is not None:
                return round(row['total'], 2)

            return 0.0

    def insert_tier_history(self, record: dict) -> None:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO tier_history (id, customer_id, order_id, tier, date, total_base_at_change, change_reason)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record['id'],
                    record['customer_id'],
                    record.get('order_id'),
                    record['tier'],
                    record['date'],
                    record['total_base_at_change'],
                    record['change_reason']
                )
            )

            connection.commit()

    def tier_already_synced_for_order(self, order_id: str) -> bool:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT 1 FROM tier_history WHERE order_id = ?", (order_id,))

            return cursor.fetchone() is not None
