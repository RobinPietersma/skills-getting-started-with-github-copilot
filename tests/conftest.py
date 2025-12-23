import copy
import pytest
from fastapi.testclient import TestClient
from src import app as application_module


@pytest.fixture
def client():
    # Make a deep copy of the initial activities so tests can mutate safely
    original = copy.deepcopy(application_module.activities)
    client = TestClient(application_module.app)
    yield client

    # Restore original state after test
    application_module.activities.clear()
    application_module.activities.update(copy.deepcopy(original))
