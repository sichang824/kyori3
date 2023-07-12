import logging
import logging.config
import os

DEFAULT_LEVEL = "DEBUG"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            'format':
            '{asctime:s} [{name:s}:{levelname:s}] [{filename:s} +{lineno:d}] {message:s}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            "style": "{",
        },
        "simple": {
            "format": "{levelname:s} {message:s}",
            "style": "{",
        },
    },
    "filters": {},
    "handlers": {
        "console": {
            # "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "console",
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "default": {
            "handlers": ["console"],
            "level": os.getenv("RPC_LOG_LEVEL", DEFAULT_LEVEL),
            "propagate": False,
        },
        "rpc": {
            "handlers": ["console"],
            "level": os.getenv("RPC_LOG_LEVEL", DEFAULT_LEVEL),
            "propagate": False,
        },
    },
}


logging.config.dictConfig(LOGGING)
logger = logging.getLogger("rpc")
