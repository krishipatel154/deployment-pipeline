from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "app_request_count",
    "Total request count of the app",
    ["method", "endpoint", "http_status"]
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Request latency",
    ["endpoint"]
)
