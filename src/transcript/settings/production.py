from .base import * 

DEBUG = False
DEBUG_PROPAGATE_EXCEPTIONS = True  # Enable's trackback


# Configuration for LOGGING
# ------------------------------------------------------------------------------

path = str(os.path.dirname(__file__)) + "/../logger/"

LOGGING_FILTERS = load_json(path + "filter.json")
LOGGING_FORMATTERS = load_json(path + "formatter.json")
LOGGING_HANDLERS = load_json(path + "handler.json")
LOGGING_LOGGERS = load_json(path + "logger_production.json")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": LOGGING_FILTERS,
    "formatters": LOGGING_FORMATTERS,
    "handlers": LOGGING_HANDLERS,
    "loggers": LOGGING_LOGGERS,
}
