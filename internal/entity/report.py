from typing import Tuple, Dict, DefaultDict
from dataclasses import dataclass, field


@dataclass
class RequestDistribution:
    """Counts requests per HTTP method.

    Attributes are counters for each supported HTTP verb. This dataclass is
    intentionally simple and optimized for incremental updates.
    """

    get:        int = 0
    post:       int = 0
    put:        int = 0
    delete:     int = 0
    patch:      int = 0
    head:       int = 0
    options:    int = 0

    def report(self, method: str):
        """Increment the counter for the given HTTP method.

        Args:
            method: HTTP method string (e.g. 'GET').

        Notes:
            Method names are looked up case-insensitively. Unknown methods
            will raise AttributeError implicitly (should not happen when
            validated earlier).
        """
        count = self.__getattribute__(method.lower())
        if count is not None:
            self.__setattr__(method.lower(), count + 1)

    def get_json(self):
        """Return a mapping of HTTP methods to counts.

        Returns:
            dict: Keys are uppercase HTTP methods, values are counts.
        """
        return {
            "GET": self.get,
            "POST": self.post,
            "PUT": self.put,
            "DELETE": self.delete,
            "PATCH": self.patch,
            "HEAD": self.head,
            "OPTIONS": self.options,
        }
        
    
    def __str__(self):
        return ("<RequestDistribution "
                f"get = {self.get} "
                f"post = {self.post} "
                f"put = {self.put} "
                f"delete = {self.delete} "
                f"patch = {self.patch} "
                f"head = {self.head} "
                f"options = {self.options}>"
        )

    __repr__ = __str__

@dataclass
class PerformanceMetrics:
    success_req:        int = 0
    client_errors:      int = 0
    server_errors:      int = 0
    average_resp_size:  int = 0

    def report(self, status_code: int) -> bool:
        """Record the given status code into performance counters.

        Args:
            status_code: Numeric HTTP status code.

        Returns:
            bool: True if the status code is considered a successful response
                (2xx), False otherwise.

        Edge cases:
            Codes outside expected ranges are ignored for client/server error
            buckets but will return False.
        """
        if status_code >= 200 and status_code < 300:
            self.success_req += 1
            return True
        elif status_code >= 400 and status_code < 500:
            self.client_errors += 1
        elif status_code >= 500 and status_code < 520:
            self.server_errors += 1
        return False

    def __str__(self):
        return ("<PerformanceMetrics "
                f"success_req = {self.success_req} "
                f"client_errors = {self.client_errors} "
                f"server_errors = {self.server_errors} "
                f"average_resp_size = {self.average_resp_size}>"
        )

    __repr__ = __str__

@dataclass
class RecentActivity:
    """Recent activity metrics for the last 24 hours.

    Attributes:
        unique_ips: Count of distinct IPs seen in the recent window.
        requests_per_hour: Mapping from integer hours-ago (0 means within last
            hour) to number of requests in that bucket.
    """

    unique_ips: int = 0
    requests_per_hour: Dict[int, int] = field(default_factory=dict)

    def __str__(self):
        return ("<RecentActivity "
                f"unique_ips = {self.unique_ips} "
                f"requests_per_hour = {self.requests_per_hour}>"
        )

    __repr__ = __str__


@dataclass
class ReportData:
    total_requests: int = 0
    unique_ips: int = 0
    total_data_transfered: int = 0

    request_dist: RequestDistribution = None
    performance_metrics: PerformanceMetrics = None

    top_active_ips: Tuple[Tuple[str, int]] = None
    top_requested_urls: Tuple[Tuple[str, int]] = None

    recent_activity: RecentActivity = None

    def __str__(self):
        return ("<ReportData "
                f"total_requests = {self.total_requests} "
                f"unique_ips = {self.unique_ips} "
                f"total_data_transfered = {self.total_data_transfered} "

                f"request_dist = {self.request_dist} "
                f"performance_metrics = {self.performance_metrics} "

                f"top_active_ips = {self.top_active_ips} "
                f"top_requested_urls = {self.top_requested_urls} "

                f"recent_activity = {self.recent_activity}>"
        )

    __repr__ = __str__

def new_report_data():
    """Create a fresh ReportData instance with initialized substructures.

    Returns:
        ReportData: New instance ready to be populated by the analyzer.
    """
    return ReportData(
        request_dist=RequestDistribution(),
        performance_metrics=PerformanceMetrics(),
        recent_activity=RecentActivity()
    )
