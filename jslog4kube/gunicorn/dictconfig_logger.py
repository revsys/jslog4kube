# pylint: disable=invalid-name, missing-docstring

import logging
from logging.config import dictConfig
import os
import sys
from importlib import import_module
from gunicorn.glogging import Logger
from .. import LOGGING, format_str


settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'demo.settings')

settings = import_module(settings_module)

class GunicornLogger(Logger):
    '''
    overrides gunicorn's Logger class to provide dictionary configuration
    capabilities
    '''
    error_fmt = format_str
    access_fmt = format_str

    def setup(self, cfg):
        self.loglevel = self.LOG_LEVELS.get(cfg.loglevel.lower(), logging.INFO)
        self.error_log.setLevel(self.loglevel)
        self.access_log.setLevel(logging.INFO)

        # set gunicorn.error handler
        if self.cfg.capture_output and cfg.errorlog != "-":
            for stream in sys.stdout, sys.stderr:
                stream.flush()

            self.logfile = open(cfg.errorlog, 'a+')
            os.dup2(self.logfile.fileno(), sys.stdout.fileno())
            os.dup2(self.logfile.fileno(), sys.stderr.fileno())

        self._set_handler(self.error_log, cfg.errorlog,
                          logging.Formatter(self.error_fmt, self.datefmt))

        # set gunicorn.access handler
        if cfg.accesslog is not None:
            self._set_handler(self.access_log, cfg.accesslog,
                              fmt=logging.Formatter(self.access_fmt),
                              stream=sys.stdout)

        # set syslog handler
        if cfg.syslog:
            self._set_syslog_handler(
                self.error_log, cfg, self.syslog_fmt, "error"
            )
            self._set_syslog_handler(
                self.access_log, cfg, self.syslog_fmt, "access"
            )

        dictConfig(LOGGING)
