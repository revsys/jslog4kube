# pylint: disable=invalid-name, missing-docstring, too-few-public-methods
"""

    The environment variables that drive this are `KUBE_META` and
    `KUBE_META_ENV_PREFIX`

    `KUBE_META` is the directory that Kubernetes metadata mountpoints
    can be found.  The default is `/etc/meta`

    `KUBE_META_ENV_PREFIX` specifies the shell variable prefix
    (defaults to `X`) that indicate a variable that should be injected
    into the log record.

    e.g.:
        X_POD_IP=100.96.1.11
        X_NODE_NAME=ip-10-70...


"""

import os

LOG_ADDS = {}

META_PATH = os.environ.get("KUBE_META", None) or "/etc/meta/"

META_ENV_PREFIX = os.environ.get("KUBE_META_ENV_PREFIX", None) or "X"

META_ENV_VAR = {
    k.lower(): v.replace('"', "")
    for k, v in os.environ.items()
    if k.startswith(META_ENV_PREFIX + "_")
}

LOG_ADDS.update(META_ENV_VAR)

try:
    with open(META_PATH + "/annotations") as fh:
        ANNO = {
            k.lower(): v.strip().replace('"', "")
            for k, v in [el.split("=") for el in fh.readlines()]
            if not k.startswith("kubernetes.io")
        }
    LOG_ADDS.update(ANNO)
except IOError:
    pass

try:
    with open(META_PATH + "/labels") as fh:
        LABELS = {
            k.lower(): v.strip().replace('"', "")
            for k, v in [el.split("=") for el in fh.readlines()]
        }
    LOG_ADDS.update(LABELS)
except IOError:
    pass

default_fields = (
    "asctime",
    "message",
    "name",
    "created",
    "filename",
    "module",
    "funcName",
    "lineno",
    "msecs",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "thread",
    "threadName",
    "levelname",
)


format_str = " ".join(
    ["%({})s".format(el) for el in default_fields + tuple(LOG_ADDS.keys())]
)
