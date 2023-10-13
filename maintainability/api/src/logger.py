import logging
import inspect
from sqlalchemy import create_engine


class DatabaseHandler(logging.Handler):
    def __init__(self, db_url):
        logging.Handler.__init__(self)
        self.db_url = db_url
        self.engine = create_engine(self.db_url)

    def emit(self, record):
        message = self.format(record)
        with self.engine.connect() as conn:
            conn.execute("INSERT INTO logs (message) VALUES (?)", (message,))


def setup_logger(db_url):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    db_handler = DatabaseHandler(db_url)
    logger.addHandler(db_handler)
    return logger


def logger(message):
    frame = inspect.currentframe().f_back
    filename = frame.f_code.co_filename
    lineno = frame.f_lineno
    logging.info(f"{message} -- File: {filename}, Line: {lineno}")
