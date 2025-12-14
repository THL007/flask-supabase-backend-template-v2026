"""Monitoring setup (Sentry, OpenTelemetry)."""
import os
from flask import current_app


def setup_monitoring(app):
    """Setup monitoring tools."""
    # Setup Sentry
    if app.config.get("SENTRY_DSN"):
        setup_sentry(app)
    
    # Setup OpenTelemetry
    if app.config.get("OTEL_EXPORTER_OTLP_ENDPOINT"):
        setup_opentelemetry(app)


def setup_sentry(app):
    """Setup Sentry error tracking."""
    try:
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration
        from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
        from sentry_sdk.integrations.redis import RedisIntegration
        
        sentry_sdk.init(
            dsn=app.config.get("SENTRY_DSN"),
            environment=app.config.get("SENTRY_ENVIRONMENT", "development"),
            traces_sample_rate=app.config.get("SENTRY_TRACES_SAMPLE_RATE", 1.0),
            integrations=[
                FlaskIntegration(),
                SqlalchemyIntegration(),
                RedisIntegration(),
            ],
            send_default_pii=False,  # Don't send PII by default
        )
        app.logger.info("Sentry initialized")
    except ImportError:
        app.logger.warning("Sentry SDK not installed, skipping Sentry setup")
    except Exception as e:
        app.logger.error(f"Failed to initialize Sentry: {e}")


def setup_opentelemetry(app):
    """Setup OpenTelemetry tracing."""
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.instrumentation.flask import FlaskInstrumentor
        from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
        from opentelemetry.instrumentation.redis import RedisInstrumentor
        
        # Set up tracer provider
        trace.set_tracer_provider(TracerProvider())
        tracer = trace.get_tracer(__name__)
        
        # Add OTLP exporter
        otlp_exporter = OTLPSpanExporter(
            endpoint=app.config.get("OTEL_EXPORTER_OTLP_ENDPOINT"),
        )
        span_processor = BatchSpanProcessor(otlp_exporter)
        trace.get_tracer_provider().add_span_processor(span_processor)
        
        # Instrument Flask
        FlaskInstrumentor().instrument_app(app)
        
        # Instrument SQLAlchemy
        SQLAlchemyInstrumentor().instrument()
        
        # Instrument Redis
        RedisInstrumentor().instrument()
        
        app.logger.info("OpenTelemetry initialized")
    except ImportError:
        app.logger.warning("OpenTelemetry not installed, skipping OpenTelemetry setup")
    except Exception as e:
        app.logger.error(f"Failed to initialize OpenTelemetry: {e}")

