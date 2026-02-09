from typing import Tuple, Dict, DefaultDict
from dataclasses import dataclass, field


@dataclass
class RequestDistribution:
    get:        int = 0
    post:       int = 0
    put:        int = 0
    delete:     int = 0
    patch:      int = 0
    head:       int = 0
    options:    int = 0

    def report(self, method: str):
        count = self.__getattribute__(method.lower())
        if count is not None:
            self.__setattr__(method.lower(), count+1)
    
    def get_json(self):
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
        """
        Save data in report

        :param int status_code: 
        :return bool: return if the status_code is success
        """
        if status_code>=200 and status_code < 300:
            self.success_req+=1
            return True
        elif status_code>=400 and status_code < 500:
            self.client_errors+=1
        elif status_code>=500 and status_code < 520:
            self.server_errors+=1
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
    unique_ips: int = 0
    requests_per_hour: Dict[str, int] = field(default_factory=DefaultDict)

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
    return ReportData(
        request_dist=RequestDistribution(),
        performance_metrics=PerformanceMetrics(),
        recent_activity=RecentActivity()
    )
