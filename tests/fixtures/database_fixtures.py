import pytest
from unittest.mock import MagicMock, patch

from api.infrastructure.sqlite_repository import SqliteCustomerRepository

@pytest.fixture
def repository():
    return SqliteCustomerRepository()

@pytest.fixture
def database():
    with patch('api.infrastructure.sqlite_repository.get_db_connection') as connection:
        connection_mock = MagicMock()
        cursor_mock = MagicMock()

        connection.return_value.__enter__.return_value = connection_mock
        connection_mock.cursor.return_value = cursor_mock

        yield cursor_mock
