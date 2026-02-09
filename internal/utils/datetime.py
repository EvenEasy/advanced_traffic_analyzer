from datetime import datetime, UTC


now_timestamp = lambda: int(round(datetime.now(UTC).timestamp()))   # Datetime now in UTC in timestamp
