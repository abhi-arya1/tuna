"""

Utilities for Tuna tests.

"""
from unittest.mock import patch
from io import StringIO
from contextlib import contextmanager

@contextmanager
def mock_stdout():
    """Context manager to mock sys.stdout."""
    new_stdout = StringIO()
    with patch('sys.stdout', new_stdout):
        yield new_stdout

@contextmanager
def mock_argv(*args):
    """Context manager to mock sys.argv."""
    with patch('sys.argv', list(args)):
        yield
