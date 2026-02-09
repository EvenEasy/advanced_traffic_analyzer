from pathlib import Path
from itertools import islice
from typing import Generator, Any
from internal.utils.datetime import now_timestamp
from internal.entity import FilterOpt, default_filter, new_report_data, ALLOWED_METHODS
from internal.entity.const import SECONDS_PER_DAY, SECONDS_PER_HOUR
from internal.logger import default_logger


ROW_TYPE = tuple[int, str, str, str, int, int]


class AdvancedTrafficAnalyzer:
    """Core analyzer that parses access logs and produces a ReportData.

    The analyzer streams the input file (generator) so it can operate on large
    files (up to the required 1,000,000 rows) without loading everything into
    memory. Filters provided via `FilterOpt` are applied per-row.

    Args:
        fltr: Optional FilterOpt instance that defines filtering rules.
    """

    def __init__(self, fltr: FilterOpt = None):
        # placeholder for loaded logs (not used to store all rows)
        self._access_logs: tuple[ROW_TYPE] = None
        # Use provided filter or default filter
        self._filter = fltr or default_filter
    
    @staticmethod
    def _read_row(row: str, *, sep=' ') -> ROW_TYPE | None:
        """
        Read access row by format: <timestamp> <ip_address> <http_method> <url> <status_code> <response_size>

        :param str row: Access log row
        :returns ROW_TYPE | None: tuple[int, str, str, str, int, int] or None if invalid
        """
        try:
            row = row.strip()
            if not row:
                # empty lines are ignored silently (common in logs)
                return None

            # Split on separator; a valid row must contain exactly 6 fields
            args = row.split(sep)
            if len(args) != 6:
                default_logger.warning(
                    "Invalid field count: expected 6, got %d: %s",
                    len(args), row[:80]
                )
                return None

            ts, ipv4, mtd, url, sts_code, resp_size = args

            # Validate timestamp: must be numeric integer
            if not ts.isnumeric():
                default_logger.warning("Invalid timestamp (not numeric): %s", ts)
                return None

            # Validate HTTP method against allowed set
            if mtd not in ALLOWED_METHODS:
                default_logger.warning("Invalid HTTP method: %s", mtd)
                return None

            # Validate numeric fields
            if not sts_code.isnumeric():
                default_logger.warning("Invalid status code (not numeric): %s", sts_code)
                return None
            if not resp_size.isnumeric():
                default_logger.warning("Invalid response size (not numeric): %s", resp_size)
                return None

            # Convert and return typed tuple
            return int(ts), ipv4, mtd, url, int(sts_code), int(resp_size)
        except Exception:
            # Any unexpected parsing error should not kill processing of the whole file
            default_logger.warning("Unexpected error parsing row: %s", row[:80])
            return None
    
    @property
    def filter(self):
        return self._filter
    
    def _filter_row(self, args):
        """
        Filter args by FilterOpt
        """
        ts, ipv4, mtd, url, sts_code, resp_size = args

        # Apply timestamp, method and status filters in sequence. Timestamp
        # filtering is done first as it is cheapest and likely to reject many rows
        return (
            self._filter.timestamp_filter(ts)
            and (not self._filter.method or mtd == self._filter.method)
            and self._filter.filter_status_code(sts_code)
        )
    
    def parse_log(self, path: str | Path, limit: int = 1_000_000) -> Generator[ROW_TYPE, Any, None]:
        """Yield parsed log rows that match the configured filter.

        This function streams the file and yields rows one by one. It is
        intentionally lightweight to support very large log files. Invalid
        lines are skipped with a warning.

        Args:
            path: Path to the access log file.
            limit: Maximum number of lines to read (safeguard for tests).

        Yields:
            ROW_TYPE tuples for rows that pass validation and filtering.

        Raises:
            FileNotFoundError: If the provided file path does not exist.
            IOError: For other I/O related errors.
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in islice(f, limit):
                    row_data = self._read_row(line)
                    if row_data and self._filter_row(row_data):
                        yield row_data
        except FileNotFoundError as e:
            default_logger.error(f"Log file not found: {path}")
            raise
        except IOError as e:
            default_logger.error(f"Error reading log file: {e}")
            raise
    
    def get_report(self, path: str | Path, limit: int = 1_000_000):
        report = new_report_data()

        # Frequency maps for top-N calculations. Memory usage proportional to
        # the number of unique IPs and URLs (expected << total rows in practice).
        ip_request_count: dict[str, int] = {}
        url_request_count: dict[str, int] = {}

        # Sum of response sizes for successful requests (2xx). Using a clear
        # variable name helps readability.
        success_received_bytes: int = 0

        # Time window parameters: compute cutoff timestamp for "recent" activity
        now_ts = now_timestamp()
        start_ts = now_ts - SECONDS_PER_DAY  # last 24 hours

        # Main processing loop (single pass over the log). This is the
        # performance-critical section; keep logic simple and avoid heavy ops.
        for ts, ipv4, mtd, url, sts_code, resp_size in self.parse_log(path, limit):
            # Basic aggregations
            report.total_requests += 1
            report.total_data_transfered += resp_size

            # Track request distribution by method
            report.request_dist.report(mtd)

            # Track performance metrics and accumulate bytes for successful responses
            was_success = report.performance_metrics.report(sts_code)
            if was_success:
                success_received_bytes += resp_size

            # IP frequency and unique IP counting
            if ipv4 not in ip_request_count:
                report.unique_ips += 1
                # If the first time we see this IP and it is recent, count it
                if ts >= start_ts:
                    report.recent_activity.unique_ips += 1
                ip_request_count[ipv4] = 1
            else:
                ip_request_count[ipv4] += 1

            # URL frequency
            url_request_count[url] = url_request_count.get(url, 0) + 1

            # Recent activity per hour (bucket by hours ago)
            if ts >= start_ts and ts <= now_ts:
                hour = int((now_ts - ts) / SECONDS_PER_HOUR)
                report.recent_activity.requests_per_hour[hour] = (
                    report.recent_activity.requests_per_hour.get(hour, 0) + 1
                )

        # Compute average response size for successful requests (2xx), guarded
        # against division by zero.
        if report.performance_metrics.success_req > 0:
            report.performance_metrics.average_resp_size = (
                success_received_bytes / report.performance_metrics.success_req
            )

        # Prepare top lists sorted by count (descending). Keep them as tuples
        # to make them immutable and easy to display.
        report.top_active_ips = tuple(
            sorted(tuple(ip_request_count.items()), key=lambda tup: tup[1], reverse=True)
        )
        report.top_requested_urls = tuple(
            sorted(tuple(url_request_count.items()), key=lambda tup: tup[1], reverse=True)
        )

        return report
            
