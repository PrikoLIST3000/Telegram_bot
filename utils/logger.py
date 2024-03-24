import logging
from config_reader import config

logger = logging.getLogger('BOT_LOG')
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler(config.log_file, mode='w', encoding="UTF-8")

formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
