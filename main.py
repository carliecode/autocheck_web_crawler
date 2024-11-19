import logging
from utils import LOG_FILE_NAME, PrometheusLoggingHandler
import process_data
import spider

# Configure logging
logging.basicConfig(
    filename=LOG_FILE_NAME,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.getLogger().addHandler(PrometheusLoggingHandler())

def run_etl():
    """Main function to execute spider and process data modules."""
    try:
        spider.main()
        process_data.main()
    except Exception as e:
        logging.error(f'An error has occurred: {e}')
        raise

if __name__ == '__main__':
    run_etl()
