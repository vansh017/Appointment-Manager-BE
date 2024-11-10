# TODO create logging functionality

import os
from logging.handlers import RotatingFileHandler
import logging


class RequestIdFilter(logging.Filter):

    def __init__(self, request_id=None):
        super().__init__()
        self.request_id = request_id

    def filter(self, record):
        record.request_id = self.request_id

        msg = record.getMessage()
        # "{'status': 'success'" add this line in
        # list to prevent printing response of API
        if any(key in msg for key in ["jwks_config"]):
            # skipping records with these strings in logs ...
            return False

        return True


class LogFormatter(logging.Formatter):
    """
    Custom log formatter for colored logs in console
    """
    ORANGE = '\033[91m'
    LIGHT_BLACK = "\033[90m"
    LIGHT_RED = "\033[91m"
    LIGHT_GREEN = "\033[92m"
    LIGHT_YELLOW = "\033[93m"
    LIGHT_BLUE = "\033[94m"
    LIGHT_MAGENTA = "\033[95m"
    LIGHT_CYAN = "\033[96m"
    LIGHT_WHITE = "\033[97m"
    MAGENTA = "\033[35m"
    BLUE = '\x1b[38;5;39m'
    CYAN = "\033[36m"
    YELLOW = '\x1b[38;5;226m'
    RED = '\x1b[38;5;196m'
    BOLD_RED = '\x1b[31;1m'
    RESET = '\x1b[0m'
    log_format = "%(levelname)s: (%(asctime)s) %(funcName)s - %(message)s"
    #  ---request_id for every API -- time ---- log level name --- func name ---- logged message

    def __init__(self):
        super().__init__()
        self.fmt = LogFormatter.log_format
        self.FORMATS = {
            logging.DEBUG: self.LIGHT_MAGENTA + self.fmt + self.RESET,
            logging.INFO: self.LIGHT_CYAN + self.fmt + self.RESET,
            logging.WARNING: self.LIGHT_YELLOW + self.fmt + self.RESET,
            logging.ERROR: self.LIGHT_RED + self.fmt + self.RESET,
            logging.CRITICAL: self.MAGENTA + self.fmt + self.RESET
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record=record)


def setup_log(logger_name, log_level=logging.DEBUG):
    env = os.environ.get("env", "dev")
    log_level = logging.DEBUG if env == "dev" \
        else logging.INFO

    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    log_format = logging.Formatter("%(asctime)s: %(levelname)s => %(funcName)s | %(message)s")

    # handler for writing logs in file
    file_handler = logging.FileHandler("app_logs/logs/app.log")
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    # handler for writing logs in console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(LogFormatter())
    logger.addHandler(console_handler)

    # rotating file handler for backup files ... incase the file becomes large
    rotating_files_handler = RotatingFileHandler(filename="app_logs/logs/app.log",
                                                 maxBytes=2000000, backupCount=5)
    logger.addHandler(rotating_files_handler)

    # oauth lib logger
    oauth_logger = logging.getLogger("oauthlib")
    oauth_logger.setLevel(log_level)
    oauth_logger.addHandler(file_handler)
    oauth_logger.addHandler(console_handler)
    oauth_logger.addFilter(RequestIdFilter(request_id=None))

    # check sqlalchemy event listener logs for this
    #     def before_cursor_execute(
    #         self, conn, cursor, statement, parameters, context, executemany
    #     ): >> before_cursor_execute is a function in sqlalchemy events

    # weasyprint_logger = logging.getLogger("weasyprint")
    # weasyprint_logger.setLevel(logging.DEBUG)
    # weasyprint_logger.addHandler(console_handler)
    # weasyprint_logger.addFilter(RequestIdFilter(request_id="weasyprint_logger_id"))

    # @event.listens_for(Engine, "before_cursor_execute")
    # def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    #     conn.info.setdefault("query_start_time", []).append(time.time())
    #     logger.debug("Start Query: %s", statement)
    #
    # @event.listens_for(Engine, "after_cursor_execute")
    # def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    #     total = time.time() - conn.info["query_start_time"].pop(-1)
    #     logger.debug("Query Complete!")
    #     logger.debug("Total Time: %f", total)

    return logger
