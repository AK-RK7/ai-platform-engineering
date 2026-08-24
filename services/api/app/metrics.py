from prometheus_client import Counter, Histogram


API_REQUESTS_TOTAL = Counter(
    "api_requests_total",
    "Total number of API requests",
    ["method", "endpoint", "status_code"],
)


API_REQUEST_DURATION_SECONDS = Histogram(
    "api_request_duration_seconds",
    "API request duration in seconds",
    ["method", "endpoint"],
)