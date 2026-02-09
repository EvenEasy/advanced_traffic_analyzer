from datetime import datetime


now_timestamp = lambda: int(round(datetime.utcnow().timestamp()))   # Datetime now in UTC in timestamp
