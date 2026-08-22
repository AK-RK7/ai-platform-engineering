import os

from fastapi import FastAPI

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import (
    SERVICE_NAME,
    SERVICE_VERSION,
    Resource,
)
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def configure_telemetry(app: FastAPI) -> None:
    resource = Resource.create(
        {
            SERVICE_NAME: "ai-platform-api",
            SERVICE_VERSION: "0.3",
            "deployment.environment": os.getenv(
                "DEPLOYMENT_ENVIRONMENT",
                "development",
            ),
        }
    )

    provider = TracerProvider(resource=resource)

    trace.set_tracer_provider(provider)

    endpoint = os.getenv(
        "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT",
        "http://otel-collector:4318/v1/traces",
    )

    exporter = OTLPSpanExporter(
        endpoint=endpoint,
    )

    processor = BatchSpanProcessor(exporter)

    provider.add_span_processor(processor)

    FastAPIInstrumentor.instrument_app(app)