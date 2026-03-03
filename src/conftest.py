import pytest
from unittest.mock import patch


@pytest.fixture(autouse=True)
def no_smtp(request):
    """Prevent all tests from making real SMTP connections."""
    with patch('dictionary_service.sql_database.sql_database.send_email', return_value=None):
        yield
