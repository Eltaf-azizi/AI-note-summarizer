import os
import pytest

@pytest.fixture(autouse=True)
def set_mock_backend_env(monkeypatch):
    # Use the mock backend for tests (no API/network)
    monkeypatch.setenv("SUM_BACKEND", "mock")
