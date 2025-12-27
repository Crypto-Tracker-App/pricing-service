from dotenv import load_dotenv
load_dotenv()
from app import create_app

from app.utils.logger import setup_logging, get_logger
setup_logging()

logger = get_logger(__name__)


app = create_app()

if __name__ == '__main__':
    logger.info("Starting Flask application", extra={"version": "1.0.0"})
    app.run(host='0.0.0.0', port=12000, debug=True)