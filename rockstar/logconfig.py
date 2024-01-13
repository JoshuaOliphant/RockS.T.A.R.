import os
import logging
from rich.logging import RichHandler
import json


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "source": {
                "file": record.pathname,
                "line": record.lineno,
            },
            "msg": record.getMessage()
        }
        if record.exc_info:
            log_record['exc_info'] = self.formatException(record.exc_info)
        try:
            return json.dumps(log_record)
        except TypeError:
            return json.dumps({"message": "Failed to serialize log record"})


def setup_logging():
    # Set up the root logger
    logging.basicConfig(
        level=os.getenv('LOG_LEVEL', logging.DEBUG),
        handlers=[RichHandler(rich_tracebacks=True, show_path=False)])
    # Modify the root logger to use the JSON formatter
    for handler in logging.root.handlers:
        handler.setFormatter(JsonFormatter())