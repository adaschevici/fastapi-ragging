from pathlib import Path

from .custom_logging import CustomizeLogger

config_path = Path(__file__).with_name("logging.config.json")

logger = CustomizeLogger.make_logger(config_path)

