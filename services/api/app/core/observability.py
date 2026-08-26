import time
from fastapi import Request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

# Initialize OpenTelemetry Tracer
provider = TracerProvider()
provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("ecrip.api")

# Prometheus Metrics for ECRIP Services
REQUEST_COUNT = Counter(
    "ecrip_http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint", "status_code"]
)
REQUEST_LATENCY = Histogram(
    "ecrip_http_request_duration_seconds",
    "HTTP Request Latency",
    ["endpoint"]
)
AGENT_EXECUTION_LATENCY = Histogram(
    "ecrip_agent_execution_seconds",
    "LangGraph Agent Execution Latency",
    ["agent_name"]
)
RAG_RETRIEVAL_PRECISION = Histogram(
    "ecrip_rag_retrieval_precision",
    "Hybrid RAG Retrieval Precision Score",
    ["pipeline_stage"]
)

async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    path = request.url.path
    method = request.method
    
    with tracer.start_as_current_span(f"{method} {path}") as span:
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception as e:
            span.record_exception(e)
            status_code = 500
            raise
        finally:
            duration = time.time() - start_time
            REQUEST_COUNT.labels(method=method, endpoint=path, status_code=status_code).inc()
            REQUEST_LATENCY.labels(endpoint=path).observe(duration)
            
        return response