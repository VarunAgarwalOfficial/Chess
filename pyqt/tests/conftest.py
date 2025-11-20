"""
Pytest configuration and shared fixtures for PyQt6 Chess tests

This module provides:
- QApplication setup
- Shared fixtures
- Test configuration
"""

import pytest
import sys
import os
from PyQt6.QtWidgets import QApplication

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


@pytest.fixture(scope="session", autouse=True)
def qapp_session():
    """
    Session-wide fixture providing QApplication instance

    This fixture is automatically used by all tests.
    QApplication is created once per test session.
    """
    if not QApplication.instance():
        app = QApplication([])
    else:
        app = QApplication.instance()

    yield app

    # Cleanup is not recommended for QApplication in pytest
    # as it causes issues with test execution


@pytest.fixture
def qapp():
    """
    Function-wide fixture providing QApplication instance

    Use this when you need the app instance in a test
    """
    return QApplication.instance()


@pytest.fixture
def cleanup_timer():
    """
    Fixture to clean up timers after tests

    Prevents "QCoreApplication::sendPostedEvents() called recursively" errors
    """
    yield

    # Give Qt some time to process pending events
    from PyQt6.QtCore import QCoreApplication
    QCoreApplication.processEvents()


@pytest.fixture(autouse=True)
def qt_sync(cleanup_timer):
    """
    Auto-used fixture to synchronize Qt event loop
    """
    from PyQt6.QtCore import QCoreApplication
    QCoreApplication.processEvents()
    yield
    QCoreApplication.processEvents()


# ============================================================================
# PYTEST CONFIGURATION
# ============================================================================

def pytest_configure(config):
    """Configure pytest"""
    # Add custom markers
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "ui: marks tests that require GUI (requires display)"
    )


# ============================================================================
# TEST COLLECTION HOOKS
# ============================================================================

def pytest_collection_modifyitems(config, items):
    """
    Modify test collection to add markers based on test characteristics
    """
    for item in items:
        # Mark tests with 'integration' in the class name
        if "Integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)

        # Mark tests with 'slow' in the name
        if "slow" in item.nodeid.lower():
            item.add_marker(pytest.mark.slow)
