import pytest

from flask_interface.library.app import create_app
from flask_interface.library.settings import TestConfig


@pytest.yield_fixture(scope='function')
def app():
    return create_app(TestConfig)
