# pylint: disable=missing-docstring
"""

This is the default logging config dictionary.

Of note:

  * the format string (`format_str`) is a a space-delimited series of
    python logging attributes that include the attributes derived from
    the kubernetes environment and/or meta-data files.

    TODO:
        KubeMetaInject: support exclusion and inclusion arguments
        Since `format_str` is derived from a list of built-in and
        kube-derived keys, manipulating this list before it is applied
        to the log record is a good place for this sort of thing.

        In addition, having `format_str` always reflect the list
        of desired attributes will avoid having to deal with manual
        maintenance of said format string.

    (https://docs.python.org/3.5/library/logging.html#logrecord-attributes)

  * If `gunicorn` is not in play, the `gunicorn.` loggers and the `json-access`
    formatter can be left off
"""

from .. import format_str

DATEFORMAT = "%Y-%m-%dT%H:%M:%S,%03d"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": "%(message)s"},
        "json": {
            "format": format_str,
            "datefmt": DATEFORMAT,
            "()": "pythonjsonlogger.json.JsonFormatter",
        },
        "json-access": {
            "datefmt": DATEFORMAT,
            "format": format_str + "%(access)",
            "()": "pythonjsonlogger.json.JsonFormatter",
        },
    },
    "filters": {"default": {"()": "jslog4kube.kube.metadata_injector.KubeMetaInject"}},
    "handlers": {
        "json-stdout": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "json",
            "filters": ["default"],
        },
        "default": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "default",
            "filters": ["default"],
        },
    },
    "loggers": {
        "efk": {
            "handlers": ["json-stdout"],
            "propagate": True,
            "level": "INFO",
            "filters": ["default"],
            "formatters": ["json"],
        },
        "demo": {
            "handlers": ["json-stdout"],
            "propagate": True,
            "level": "INFO",
            "filters": ["default"],
            "formatters": ["json"],
        },
        "django": {
            "handlers": ["json-stdout"],
            "propagate": True,
            "level": "INFO",
            "filters": ["default"],
            "formatters": ["json"],
        },
        "gunicorn": {
            "handlers": ["json-stdout"],
            "formatters": ["json"],
            "propagate": False,
            "level": "ERROR",
        },
        "gunicorn.access": {
            "handlers": ["json-stdout"],
            "formatters": ["json-access"],
            "propagate": False,
            "level": "INFO",
        },
        "gunicorn.error": {
            "handlers": ["json-stdout"],
            "formatters": ["json"],
            "propagate": False,
            "level": "INFO",
        },
        "requests": {
            "handlers": ["json-stdout"],
            "formatters": ["json"],
            "propagate": True,
            "filters": ["default"],
            "level": "INFO",
        },
    },
}
