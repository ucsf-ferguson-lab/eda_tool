import os
import logging
import uptrace


def setup_otel_logging() -> None:
    dsn_value: str | None = os.getenv("OTEL")
    if not dsn_value:
        raise ValueError("OTEL not found in environment")

    uptrace.configure_opentelemetry(
        dsn=dsn_value,
        service_name="eda_tool",
        service_version="0.1.0",
        logging_level=logging.INFO,
    )
