# pylint: disable=missing-docstring

from ..bootstrap import format_str

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(message)s'
        },
        'json': {
            'format': format_str,
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
        },
        'json-access': {
            'format': format_str + '%(access)',
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
        },
    },
    'filters': {
        'default': {
            '()': 'demo.kube_log_filter.KubeMetaInject',
        },
    },
    'handlers': {
        'json-stdout': {
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'json',
            'filters': ['default'],
        },
        'default': {
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'default',
            'filters': ['default'],
        },
    },
    'loggers': {
        'efk': {
            'handlers': ['json-stdout',],
            'propagate': True,
            'level':'DEBUG',
            'filters': ['default'],
            'formatters': ['json'],
        },
        'demo': {
            'handlers': ['json-stdout',],
            'propagate': True,
            'level':'DEBUG',
            'filters': ['default'],
            'formatters': ['json'],
        },
        'django': {
            'handlers': ['json-stdout',],
            'propagate': True,
            'level': 'INFO',
            'filters': ['default'],
            'formatters': ['json'],
        },
        'gunicorn': {
            'handlers': ['json-stdout'],
            'formatters': ['json'],
            'propagate': False,
            'level':'ERROR',
        },
        'gunicorn.access': {
            'handlers': ['json-stdout'],
            'formatters': ['json-access'],
            'propagate': False,
            'level':'DEBUG',
        },
        'gunicorn.error': {
            'handlers': ['json-stdout'],
            'formatters': ['json'],
            'propagate': False,
            'level':'INFO',
        },
        'requests': {
            'handlers': ['json-stdout',],
            'formatters': ['json'],
            'propagate': True,
            'filters': ['default'],
            'level':'DEBUG',
        },
    }
}

