# pylint: disable=invalid-name, missing-docstring, too-few-public-methods
"""

    This is a straight-forward record augmenting log filter.

    The `gunicorn.access` logic is driven by an oddly delimited
    gunicorn access-log format string

    The access log format.

    ===========  ===========
    Identifier   Description
    ===========  ===========
    h            remote address
    l            ``'-'``
    u            user name
    t            date of the request
    r            status line (e.g. ``GET / HTTP/1.1``)
    m            request method
    U            URL path without query string
    q            query string
    H            protocol
    s            status
    B            response length
    b            response length or ``'-'`` (CLF format)
    f            referer
    a            user agent
    T            request time in seconds
    D            request time in microseconds
    L            request time in decimal seconds
    p            process ID
    {Header}i    request header
    {Header}o    response header
    {Variable}e  environment variable
    ===========  ===========

`!` is '='
'|' delimits the attribute
'remote!%(h)s|method!%(m)s|url-path!%(U)s|query!%(q)s|username!%(u)s|...`

"""
import logging
from .. import LOG_ADDS


class KubeMetaInject(logging.Filter):
    def filter(self, record):
        for k, v in LOG_ADDS.items():
            setattr(record, k, v)

        if record.name == "gunicorn.access":
            msg = record.getMessage()
            try:
                msg_elements = {
                    k: v for k, v in [el.split("!") for el in msg.split("|")]
                }
                record.access = msg_elements
                record.msg = "(access record)"
            except ValueError:
                pass

        return True

