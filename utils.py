import logging
import time

from opentelemetry import trace

logging.basicConfig(filename='app.log', level=logging.INFO)

def current_milli_time():
    return round(time.time() * 1000)

class LoggerAdapter(logging.LoggerAdapter):
    def __init__(self, logger):
        super(LoggerAdapter, self).__init__(logger, {})

    def process(self, msg, kwargs):
        span_id = f'{trace.get_current_span().get_span_context().span_id:x}'
        trace_id = f'{trace.get_current_span().get_span_context().trace_id:x}'
        return '{dt.span_id=%s, dt.trace_id=%s} %s' % (span_id, trace_id, msg), kwargs