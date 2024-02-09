import json
import os

from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.http._log_exporter import \
    OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import \
    OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import \
    OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics._internal.instrument import (Counter,
                                                            UpDownCounter)
from opentelemetry.sdk.metrics.export import (AggregationTemporality,
                                              ConsoleMetricExporter,
                                              PeriodicExportingMetricReader)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider, sampling
from opentelemetry.sdk.trace.export import (BatchSpanProcessor,
                                            ConsoleSpanExporter)
from opentelemetry.semconv.resource import ResourceAttributes

DT_API_URL = os.environ.get('DT_API_URL')
DT_API_TOKEN = os.environ.get('DT_API_TOKEN')

"""A class for controlling custom OpenTelemetry behavior"""
class CustomOpenTelemetry():
    def __init__(self):
        self.setup_exporters()

    """Sets up OpenTelemetry Trace & Metrics export"""
    def setup_exporters(self):

        # -----------------------
        # Basic resource details
        # -----------------------
        merged = dict()
        for name in [
            "dt_metadata_e617c525669e072eebe3d0f08212e8f2.json",
            "/var/lib/dynatrace/enrichment/dt_metadata.json",
            "/var/lib/dynatrace/enrichment/dt_host_metadata.json"
        ]:
            try:
                data = ''
                with open(name) as f:
                    data = json.load(f if name.startswith("/var") else open(f.read()))
                    merged.update(data)
            except:
                pass

        merged.update({
            "service.name": "pysrvc svc on port 8090",
            "service.version": "v1.0.0",
        })
        resource = Resource.create(merged)
        
        # -------------------------------------------------------------------------------
        # Set up trace export
        # https://docs.dynatrace.com/docs/extend-dynatrace/opentelemetry/overview/traces
        # -------------------------------------------------------------------------------
        tracer_provider = TracerProvider(
            sampler=sampling.ALWAYS_ON,
            resource=resource
        )
        tracer_provider.add_span_processor(
            BatchSpanProcessor(OTLPSpanExporter(
                endpoint = DT_API_URL + "/v1/traces",
                headers = {"Authorization": "Api-Token " + DT_API_TOKEN}
            ))
        )
        # This is optional - but helpful for debugging purposes
        tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

        trace.set_tracer_provider(tracer_provider)
        
        # --------------------------------------------------------------------------------
        # Set up metrics export
        # https://docs.dynatrace.com/docs/extend-dynatrace/opentelemetry/overview/metrics
        # --------------------------------------------------------------------------------
        meterProvider = MeterProvider(
            resource=resource,
            metric_readers=[
            PeriodicExportingMetricReader(
                OTLPMetricExporter(
                    endpoint=DT_API_URL + "/v1/metrics",
                    preferred_temporality={
                        Counter: AggregationTemporality.DELTA,
                        UpDownCounter: AggregationTemporality.DELTA
                    }
                )
            ),
            # This is optional - but helpful for debugging purposes
            PeriodicExportingMetricReader(ConsoleMetricExporter())
        ])        
        metrics.set_meter_provider(meterProvider)

ot = CustomOpenTelemetry()