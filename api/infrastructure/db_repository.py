import sqlite3
from typing import Optional, List
from datetime import datetime, timedelta

import api.domain.services as domain_services
from api.application.ports import CustomerRepository
from api.domain.constants import Tier
from api.domain.models import Customer, Order, TierHistoryItem


DB_FILE = "hamster_foods.db"

def get_db_connection():
    connection = sqlite3.connect(DB_FILE)
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

        with get_db_connection() as conn:
            cursor = conn.cursor()
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

    def sync_user_tier(self, customer_id: str, reason: str):

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("BEGIN IMMEDIATE")
            try:
                cursor.execute(
                    "SELECT tier FROM tier_history WHERE customer_id = ? ORDER BY date DESC LIMIT 1",
                    (customer_id,)
                )

                current_tier_row = cursor.fetchone()
                current_tier = Tier(current_tier_row['tier']) if current_tier_row else Tier.NO_TIER
                ten_days_ago = datetime.now() - timedelta(days=10)

                cursor.execute(
                    "SELECT SUM(amount_base) as total FROM orders WHERE customer_id = ? AND created_at >= ?",
                    (customer_id, ten_days_ago.strftime('%Y-%m-%d %H:%M:%S'))
                )

                total_row = cursor.fetchone()
                current_total_base = total_row['total'] if total_row and total_row['total'] is not None else 0.0
                new_tier = domain_services.get_tier_for_amount(current_total_base)

                if new_tier != current_tier:
                    cursor.execute(
                        """
                        INSERT INTO tier_history (id, customer_id, tier, date, total_base_at_change, change_reason)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (
                            f"th-{customer_id}-{datetime.now().timestamp()}",
                            customer_id,
                            new_tier.value,
                            datetime.now().isoformat(),
                            round(current_total_base, 2),
                            reason
                        )
                    )
                
                conn.commit()

            except Exception as e:
                conn.rollback()
                print(f"Error syncing tier for customer {customer_id}: {e}")

                raise