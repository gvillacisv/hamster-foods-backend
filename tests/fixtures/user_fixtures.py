import pytest
from datetime import datetime, timedelta

from api.domain.models import Customer, Order, TierHistoryItem, Tier

def _get_relative_datetime(days_ago: int, hour: int = 12, minute: int = 0) -> datetime:
    return (datetime.now() - timedelta(days=days_ago)).replace(hour=hour, minute=minute, second=0, microsecond=0)

@pytest.fixture
def champion_fixture():
    customer_id = 'c-01'
    customer = Customer(id=customer_id, name='Champion')
    orders = [
        Order(id='oc-03', customer_id=customer_id, amount_value=10, amount_currency='EUR', amount_base=10.00, exchange_rate=1, created_at=_get_relative_datetime(5, 18, 5)),
        Order(id='oc-04', customer_id=customer_id, amount_value=15, amount_currency='EUR', amount_base=15.00, exchange_rate=1, created_at=_get_relative_datetime(2, 10, 31)),
    ]
    history = [
        TierHistoryItem(id='th-01', tier=Tier.CHAMPION, date=_get_relative_datetime(2, 10, 31), totalAtChange=25.00, changeReason='TRANSACTION'),
        TierHistoryItem(id='th-01', tier=Tier.LOYAL, date=_get_relative_datetime(5, 18, 5), totalAtChange=10.00, changeReason='TRANSACTION'),
    ]

    return { "customer": customer, "orders": orders, "history": history }

@pytest.fixture
def newcomer_fixture():
    customer_id = 'c-02'
    customer = Customer(id=customer_id, name='Newcomer')
    orders = []
    history = []

    return { "customer": customer, "orders": orders, "history": history }

@pytest.fixture
def newbie_fixture():
    customer_id = 'c-04'
    customer = Customer(id=customer_id, name='Newbie')
    orders = [
        Order(id='oc-08', customer_id=customer_id, amount_value=5, amount_currency='EUR', amount_base=5.00, exchange_rate=1, created_at=_get_relative_datetime(4, 17, 50)),
    ]
    history = [
        TierHistoryItem(id='th-04', tier=Tier.NO_TIER, date=_get_relative_datetime(4, 17, 50), totalAtChange=0.00, changeReason='TRANSACTION'),
    ]
    
    return { "customer": customer, "orders": orders, "history": history }

@pytest.fixture
def loyal_user_fixture():
    customer_id = 'c-02'
    customer = Customer(id=customer_id, name='Loyal')
    orders = [
        Order(id='oc-05', customer_id=customer_id, amount_value=8, amount_currency='EUR', amount_base=8.00, exchange_rate=1, created_at=_get_relative_datetime(8, 16, 30)),
        Order(id='oc-06', customer_id=customer_id, amount_value=10, amount_currency='EUR', amount_base=10.00, exchange_rate=1, created_at=_get_relative_datetime(1, 11, 45)),
    ]
    history = [
        TierHistoryItem(id='th-02', tier=Tier.LOYAL, date=_get_relative_datetime(20), total_base_at_change=16.50, change_reason='TRANSACTION'),
    ]

    return { "customer": customer, "orders": orders, "history": history }

@pytest.fixture
def rooki_user_fixture():
    customer_id = 'c-03'
    customer = Customer(id=customer_id, name='Rookie')
    orders = [
        Order(id='oc-07', customer_id=customer_id, amount_value=10, amount_currency='EUR', amount_base=10.00, exchange_rate=1, created_at=_get_relative_datetime(3, 13, 0)),
    ]
    history = [
        TierHistoryItem(id='th-03', tier=Tier.ROOKIE, date=_get_relative_datetime(15), total_base_at_change=7.50, change_reason='TRANSACTION'),
    ]

    return { "customer": customer, "orders": orders, "history": history }

@pytest.fixture
def newbie_user_fixture():
    customer_id = 'c-04'
    customer = Customer(id=customer_id, name='Newbie')
    orders = [
        Order(id='oc-08', customer_id=customer_id, amount_value=5, amount_currency='EUR', amount_base=5.00, exchange_rate=1, created_at=_get_relative_datetime(4, 17, 50)),
    ]
    history = [
        TierHistoryItem(id='th-04', tier=Tier.NO_TIER, date=_get_relative_datetime(10), total_base_at_change=0.00, change_reason='TRANSACTION'),
    ]
    
    return { "customer": customer, "orders": orders, "history": history }

@pytest.fixture
def demoted_user_fixture():
    customer_id = 'c-05'
    customer = Customer(id=customer_id, name='Demoted')
    orders = [
        Order(id='oc-07', customer_id=customer_id, amount_value=9, amount_currency='EUR', amount_base=9.00, exchange_rate=1, created_at=_get_relative_datetime(11)),
    ]
    history = [
        TierHistoryItem(id='th-05', tier=Tier.ROOKIE, date=_get_relative_datetime(15), total_base_at_change=9.00, change_reason='TRANSACTION'),
        TierHistoryItem(id='th-06', tier=Tier.NO_TIER, date=_get_relative_datetime(1), total_base_at_change=0.00, change_reason='EXPIRATION'),
    ]
    
    return { "customer": customer, "orders": orders, "history": history }
