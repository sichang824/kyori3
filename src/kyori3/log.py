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


class LogRawStrings:
    exported = '%s has already exported and will be ignored.'
    exporting = "Function exporting: %s %s %s"

    heading = "Head Function: %s"
    execute = "Execute function: %s(%s, %s)"
    result = "Execute result: %s"

    load_ssl = "Loading SSL: %s %s"
    server_starting = "Server start at: %s"
    server_shutdown = "Server shutdown."

    type_setting = "Setting Content-type: %s"
    no_payload = "RPC server requires pyload, please check the request body."

    refused = "Failed to connect to the server, maybe the server is not ready."
    reset = "Failed to connect to the server, try ssl connection."


logging.config.dictConfig(LOGGING)
logger = logging.getLogger("rpc")
