REPORT_FORMAT = """
====== TRAFFIC ANALYSIS REPORT ======
Filter settings:
 - Time range: {filter_time_range}
 - Method filter: {filter_method}
 - Status filter: {filter_status}

Basic statistics:
 - Total requests: {total_requests}
 - Unique IPs: {unique_ips}
Total data transferred: <bytes> (<human_readable>)
Request distribution:
{request_dist_view}
Performance metrics:
 - Successful requests (2xx): {performance_metrics.success_req}
 - Client errors (4xx): {performance_metrics.client_errors}
 - Server errors (5xx): {performance_metrics.server_errors}
 - Average response size (2xx): {avg_rsp_size}
Top {filter.top} active IPs:
{show_top_active_ips}
Top 5 requested URLs:
{show_top_requested_urls}
Recent activity (last 24h):
 - Unique IPs: {recent_activity.unique_ips}
 - Requests per hour (last 24h): {recent_rate_by_hours}
"""
