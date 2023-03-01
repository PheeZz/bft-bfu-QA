from loguru import logger
from datetime import datetime


def setup_logger() -> None:
    logger.add(f'logs/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log',
               level='INFO', rotation='1 week', compression='zip')
