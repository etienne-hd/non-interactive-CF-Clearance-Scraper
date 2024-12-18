import logging

logger = logging.getLogger(__name__)

formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# Define color codes
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class Logger:
    @staticmethod
    def success(message: str) -> None:
        logger.debug(f"{Colors.GREEN}{message}{Colors.ENDC}")

    @staticmethod
    def error(message: str) -> None:
        logger.debug(f"{Colors.FAIL}{message}{Colors.ENDC}")

    @staticmethod
    def info(message: str) -> None:
        logger.debug(f"{Colors.CYAN}{message}{Colors.ENDC}")
