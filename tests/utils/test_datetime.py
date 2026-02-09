import time
from internal.utils.datetime import now_timestamp


def test_now_timestamp_is_int_and_close_to_now():
    ts = now_timestamp()
    assert isinstance(ts, int)

    # should be close to current time (allow a few seconds drift)
    assert abs(ts - int(time.time())) <= 5
