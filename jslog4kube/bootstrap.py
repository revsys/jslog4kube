# pylint: disable=invalid-name, missing-docstring, too-few-public-methods

import os
from importlib import import_module

settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'demo.settings')

settings = import_module(settings_module)

LOG_ADDS = {}

META_PATH = settings.K8S_META or'/etc/meta/'
META_ENV_PREFIX = settings.K8S_META_PREFIX or 'X'

if not META_ENV_PREFIX:
    META_ENV_PREFIX = 'X'

META_ENV_VAR = {
    k.lower(): v.replace('"', '')
    for k, v  in os.environ.items()
    if k.startswith(META_ENV_PREFIX + '_')
}

LOG_ADDS.update(META_ENV_VAR)

try:
    with open(META_PATH + '/annotations') as fh:
        ANNO = {
            k.lower(): v.strip().replace('"', '')
            for k, v in [
                el.split('=')
                for el in fh.readlines()
            ]
            if not k.startswith('kubernetes.io')
        }
    LOG_ADDS.update(ANNO)
except FileNotFoundError:
    pass

try:
    with open(META_PATH + '/labels') as fh:
        LABELS = {
            k.lower(): v.strip().replace('"', '')
            for k, v in [
                el.split('=')
                for el in fh.readlines()
            ]
        }
    LOG_ADDS.update(LABELS)
except FileNotFoundError:
    pass

default_fields = (
    'asctime',
    'message',
    'name',
    'created',
    'filename',
    'module',
    'funcName',
    'lineno',
    'msecs',
    'pathname',
    'process',
    'processName',
    'relativeCreated',
    'thread',
    'threadName',
    'levelname')


format_str = ' '.join([
    '%({})s'.format(el)
    for el
    in default_fields + tuple(LOG_ADDS.keys())
])
