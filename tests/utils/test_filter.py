import pytest
from internal.utils.filter import get_status_code_range


def test_get_status_code_range_empty():
    assert get_status_code_range("") == (None, None)
    assert get_status_code_range(None) == (None, None)


def test_get_status_code_range_single():
    assert get_status_code_range("200") == (200, 200)
    assert get_status_code_range(" 200 ") == (200, 200)


def test_get_status_code_range_range():
    assert get_status_code_range("400-499") == (400, 499)
    assert get_status_code_range(" 400 - 499 ") == (400, 499)
