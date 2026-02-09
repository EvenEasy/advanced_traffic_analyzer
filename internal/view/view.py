from typing import Callable
from internal.entity import FilterOpt
from internal.anazyler import ReportData, RequestDistribution
from .const import REPORT_FORMAT


class ViewReport:
    def _top_report_row(cls, pos: int, key: str, value: str, *args: str):
        return f'{pos}. {key}: {value}' + (' ' + ' '.join(args) if args else '')

    def _top_report_rows(cls, rows: tuple[tuple[str, int]], limit: int, *args: str):
        if not isinstance(rows, tuple) or not rows:
            return ""

        res = [cls._top_report_row(i, key, value, *args)for i, (key, value) in enumerate(rows[:limit], start=1)]
        return '\n'.join(res)

    def get_request_dist_view(self, data: RequestDistribution, total_req: int):
        rows = ["{0}: {1:.2f}%".format(mtd, count/total_req*100) for mtd, count in data.get_json().items() if count > 0]
        return '\n'.join(rows)
    
    def show_report(self, report: ReportData, fltr: FilterOpt, *, out: Callable[[str], None] = print):
        out(REPORT_FORMAT.format(
            filter=fltr,
            total_requests=report.total_requests,
            unique_ips=report.unique_ips,
            performance_metrics=report.performance_metrics,
            recent_activity=report.recent_activity,
            request_dist_view=self.get_request_dist_view(report.request_dist, report.total_requests),
            avg_rsp_size=report.performance_metrics.average_resp_size,
            show_top_active_ips=self._top_report_rows(report.top_active_ips, fltr.top),
            show_top_requested_urls=self._top_report_rows(report.top_requested_urls, 5, 'requests'),
            recent_rate_by_hours=report.recent_activity.requests_per_hour
            
        ))
        
    
