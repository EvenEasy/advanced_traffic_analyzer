from pathlib import Path
from itertools import islice
from typing import Generator, Any
from internal.utils.datetime import now_timestamp
from internal.entity import FilterOpt, default_filter, new_report_data, ALLOWED_METHODS


ROW_TYPE = tuple[int, str, str, str, int, int]


class AdvancedTrafficAnalyzer:

    def __init__(self, fltr: FilterOpt = None):
        self._access_logs: tuple[ROW_TYPE] = None
        self._filter = fltr or default_filter
    
    @staticmethod
    def _read_row(row: str, *, sep=' ') -> ROW_TYPE:
        """
        Read access row by format: <timestamp> <ip_address> <http_method> <url> <status_code> <response_size>

        :param str row: Access log row
        :returns ROW_TYPE: tuple[int, str, str, str, int, int]
        """

        row = row.strip()
        args = row.split(sep)
        assert len(args) == 6, "Invalid row"

        ts, ipv4, mtd, url, sts_code, resp_size = args
        assert ts.isnumeric(), "timestamp must be integer"
        assert mtd in ALLOWED_METHODS, f"Method: {mtd} not allowed"
        assert sts_code.isnumeric(), "status_code must be integer"
        assert resp_size.isnumeric(), "response_size must be integer"

        return int(ts), ipv4, mtd, url, int(sts_code), int(resp_size)
    
    @property
    def filter(self):
        return self._filter
    
    def _filter_row(self, args):
        """
        Filter args by FilterOpt
        """
        ts, ipv4, mtd, url, sts_code, resp_size = args

        return (
            self._filter.timestamp_filter(ts)
            and (not self._filter.method or mtd == self._filter.method)
            and self._filter.filter_status_code(sts_code)
        )
    
    def parse_log(self, path: str | Path, limit: int = 1_000_000) -> Generator[ROW_TYPE, Any, None]:
        with open(path, 'r', encoding='utf-8') as f:
            if not f.readable(): return []
            for i, line in enumerate(islice(f, limit)):
                if i >= limit: return
                args = self._read_row(line)
                if self._filter_row(args):
                    yield args
    
    def get_report(self, path: str | Path, limit: int = 1_000_000):
        report = new_report_data()
        user_rate: dict[str, int] = {}
        url_rate: dict[str, int] = {}
        success_reveived: int = 0

        # params
        now_ts = now_timestamp()
        start_ts = now_ts - 86_400  # recently 24 hours
        
        # proccessing
        for ts, ipv4, mtd, url, sts_code, resp_size in self.parse_log(path, limit):
            report.total_requests += 1
            report.total_data_transfered+=resp_size
            report.request_dist.report(mtd)
            success = report.performance_metrics.report(sts_code)
            if success:
                success_reveived+=resp_size

            # rate ipv4
            if ipv4 not in user_rate:
                report.unique_ips+=1
                if ts >= start_ts:
                    report.recent_activity.unique_ips+=1
                user_rate[ipv4] = 1
            else:
                user_rate[ipv4] += 1
            
            # rate url
            if url not in url_rate:
                url_rate[url]=1
            else:
                url_rate[url] += 1
            
            if ts >= start_ts:
                hour = int((now_ts-ts) / 3600)
                report.recent_activity.requests_per_hour[hour] = report.recent_activity.requests_per_hour.get(hour, 0) + 1
        
        report.performance_metrics.average_resp_size = success_reveived / report.performance_metrics.success_req # TODO: get formula
        report.top_active_ips = tuple(sorted(tuple(user_rate.items()), key=lambda tup: tup[1], reverse=True))
        report.top_requested_urls = tuple(sorted(tuple(url_rate.items()), key=lambda tup: tup[1], reverse=True))
        
        return report
            
