"""
Pytest configuration file
"""
import pytest
from base_test import BaseTest


@pytest.fixture(scope='function')
def setup_teardown():
    """Setup and teardown fixture for each test"""
    test_instance = BaseTest()
    test_instance.setup_method()
    yield test_instance
    test_instance.teardown_method()
