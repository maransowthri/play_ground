import logging


LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename='update_index.log', level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger()
logger.info("I'm here")