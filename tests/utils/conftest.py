import sys
import types
import importlib

import pytest


@pytest.fixture(autouse=True)
def stub_internal_modules(monkeypatch):
    """
    analyzer.py imports:
      from internal.utils.datetime import now_timestamp
      from internal.entity import FilterOpt, default_filter, new_report_data, ALLOWED_METHODS

    In tests we create minimal stubs in sys.modules so analyzer.py can import.
    """
    # Create module internal, internal.utils, internal.utils.datetime
    internal = types.ModuleType("internal")
    internal_utils = types.ModuleType("internal.utils")
    internal_utils_datetime = types.ModuleType("internal.utils.datetime")

    # Use now_timestamp from local datetime.py (uploaded file)
    dt = importlib.import_module("datetime")  # <-- imports your datetime.py if it's on PYTHONPATH
    internal_utils_datetime.now_timestamp = dt.now_timestamp

    # Create internal.entity stub
    internal_entity = types.ModuleType("internal.entity")

    class DummyFilterOpt:
        def __init__(self, start=None, end=None, method=None, status=None):
            self.start = start
            self.end = end
            self.method = method
            self.status = status

        def timestamp_filter(self, ts: int) -> bool:
            return True

        def filter_status_code(self, code: int) -> bool:
            return True

    internal_entity.FilterOpt = DummyFilterOpt
    internal_entity.ALLOWED_METHODS = {"GET", "POST"}

    # default_filter instance
    internal_entity.default_filter = DummyFilterOpt()

    # not needed for these basic tests, but must exist for import
    internal_entity.new_report_data = lambda: object()

    # Inject into sys.modules
    monkeypatch.setitem(sys.modules, "internal", internal)
    monkeypatch.setitem(sys.modules, "internal.utils", internal_utils)
    monkeypatch.setitem(sys.modules, "internal.utils.datetime", internal_utils_datetime)
    monkeypatch.setitem(sys.modules, "internal.entity", internal_entity)

    yield
