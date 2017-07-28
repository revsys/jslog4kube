# pylint: disable=invalid-name, missing-docstring, too-few-public-methods
'''
Make it easy to emit JSON structured logging to stdout for Python apps and
WSGI apps running inside Gunicorn.
'''

__version__ = '1.0.1'

import logging
import time
from pythonjsonlogger.jsonlogger import JsonFormatter
from .bootstrap import LOG_ADDS, format_str
from .kube.log_config import LOGGING
from .kube.metadata_injector import KubeMetaInject

JsonFormatter.converter = time.gmtime


try:
    from .gunicorn.dictconfig_logger import GunicornLogger
    HAS_GUNICORN = True
except ImportError:
    HAS_GUNICORN = False


__all__ = ['LOG_ADDS', 'format_str', 'LOGGING']
