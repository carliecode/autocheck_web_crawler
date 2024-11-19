import logging
from datetime import datetime 
from prometheus_client import CollectorRegistry, Gauge, Counter, push_to_gateway

# Constants for URLs, paths, and user agents
DOWNLOADED_FILE = 'data/jiji_cars.csv'
ARCHIVE_FOLDER = 'data/archive'
USER_AGENTS = [
    "Mozilla/5.0",
    "Chrome/91.0.4472.114",
    "Safari/605.1.15",
    "Firefox/89.0",
    "Edge/91.0.864.37"
]
PAGE_URL = 'https://jiji.ng/cars'

PUSHGATEWAY_URL = 'http://localhost:9091'
PROMETHEUS_JOB_NAME = 'Car_Price_Spider'
LOG_FILE_NAME = f"logs/cars_website_crawler_{datetime.today().strftime('%Y-%m-%d')}.log"


# Initialize Prometheus registry and counters
registry = CollectorRegistry()
log_counter = Counter('log_entries', 'Count of log entries by level', ['level'], registry=registry)

class PrometheusLoggingHandler(logging.Handler):
    """Custom logging handler to push log counters to Prometheus."""

    def emit(self, record):
        """Emit a record and update the log counter."""
        if record.levelname == 'INFO':
            log_counter.labels(level='info').inc()
        elif record.levelname == 'WARNING':
            log_counter.labels(level='warning').inc()
        elif record.levelname == 'ERROR':
            log_counter.labels(level='error').inc()
        
        try:
            push_to_gateway(PUSHGATEWAY_URL, job=PROMETHEUS_JOB_NAME, registry=registry)
        except Exception as e:
            logging.error(f'Prometheus: {e}')