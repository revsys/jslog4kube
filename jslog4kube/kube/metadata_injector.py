# pylint: disable=invalid-name, missing-docstring, too-few-public-methods

import logging
from ..constants import LOG_ADDS


class KubeMetaInject(logging.Filter):

    def filter(self, record):
        for k, v in LOG_ADDS.items():
            setattr(record, k, v)

        if record.name == 'gunicorn.access':
            msg = record.msg
            msg_elements = {
                k: v
                for k, v in [el.split('!')
                             for el in msg.split('|')]
            }
            record.access = msg_elements
            record.msg = "(access record)"

        return True


