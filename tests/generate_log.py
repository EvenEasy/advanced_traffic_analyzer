import random
from datetime import datetime, UTC

OUTPUT_FILE = "tests/test_logs.log"
LINES_COUNT = 1_000_000
BASE_TIMESTAMP = int(round(datetime.now(UTC).timestamp()))

ip_pool = [
    "192.168.1.10",
    "192.168.1.11",
    "192.168.1.12",
    "10.0.0.5",
    "10.0.0.10",
    "172.16.0.2",
    "8.8.8.8",
    "34.201.45.12",
    "185.23.44.11"
]

methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]

urls = [
    "/",
    "/home",
    "/profile",
    "/admin",
    "/dashboard",
    "/api/login",
    "/api/register",
    "/api/data",
    "/api/upload",
    "/logout"
]

status_codes = [200, 201, 204, 400, 401, 403, 404, 500]

with open(OUTPUT_FILE, "w") as f:
    for i in range(LINES_COUNT):
        timestamp = BASE_TIMESTAMP - random.randint(0, 86400)
        ip = random.choice(ip_pool)
        method = random.choice(methods)
        url = random.choice(urls)
        status = random.choice(status_codes)
        response_size = random.randint(50, 5000)

        line = f"{timestamp} {ip} {method} {url} {status} {response_size}\n"
        f.write(line)

print(f"Generated {LINES_COUNT} log lines into {OUTPUT_FILE}")
