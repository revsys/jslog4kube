
# jslog4kube (python/JSON logging for kubernetes pod/containers)


## Why?

  * provide a JSON-to-stdout setup for python
  * provide the same JSON-to-stdout setup for [gunicorn](http://gunicorn.org)
  * because creating complex log collector configs to handle whatever
    that other person thought was a good-idea-at-the-time is for the birds.

We want to make it easier for our clients and ourselves to start new projects
that emit good logging.

### making it go

Two environment variables configure this module:

  * `KUBE_META`: specifies the mount-point for the Kubernetes downward-API
  [volumes](https://kubernetes.io/docs/tasks/inject-data-application/downward-api-volume-expose-pod-information/) bits (default: /etc/meta)
  * `KUBE_META_ENV_PREFIX`: the textual prefix for any
  [environment variables](https://kubernetes.io/docs/tasks/inject-data-application/environment-variable-expose-pod-information/)
  targetted for inclusion in this pod’s log records (default: X)

----



---------------------------------------------------------------------------------------
 These bits have been verified to be functional under python 3.9+
---------------------------------------------------------------------------------------

----



```python

from logging.config import dictConfig
from jslog4kube import LOGGING

dictConfig(LOGGING)

```


#### From Django

project `settings.py`
```python

from jslog4kube import LOGGING

```

#### [gunicorn](http://gunicorn.org)

gunicorn.conf
```python

access_log_format = 'remote!%({X-Forwarded-For}i)s|method!%(m)s|url-path!%(U)s|query!%(q)s|username!%(u)s|protocol!%(H)s|status!%(s)s|response-length!%(b)s|referrer!%(f)s|user-agent!%(a)s|request-time!%(L)s'
accesslog = '-'
logger_class = 'jslog4kube.GunicornLogger'

```

gunicorn CLI
```bash

gunicorn -c /path/to/gunicorn.conf [rest of your options here]
```


This will produce the following kind of output:

```json
{
  "asctime": "2017-07-12 16:07:34,624",
  "message": "Booting worker with pid: 6801",
  "name": "gunicorn.error",
  "created": 1499893654.6243172,
  "filename": "glogging.py",
  "module": "glogging",
  "funcName": "info",
  "lineno": 247,
  "msecs": 624.3171691894531,
  "pathname": "/home/gladiatr/.virtualenvs/json-logs-for-kube/lib/python3.6/site-packages/gunicorn/glogging.py",
  "process": 6801,
  "processName": "MainProcess",
  "relativeCreated": 70.62673568725586,
  "thread": 140275859264576,
  "threadName": "MainThread",
  "levelname": "INFO",
  "x_node_name": "ip-10-70-59-190.eu-central-1.compute.internal",
  "x_sa_name": "default",
  "x_pod_ip": "100.96.1.11",
  "build": "5000",
  "builder": "Stephen Spencer",
  "image": "gladiatr72/kube-demo",
  "version": "1.0.2",
  "app": "kube-demo",
  "env": "dev",
  "pod-template-hash": "2802633501",
  "something": "else"
}
{
  "asctime": "2017-07-12 21:08:16,354",
  "message": "in view: Chameleon",
  "name": "efk.views",
  "created": 1499893696.3544216,
  "filename": "views.py",
  "module": "views",
  "funcName": "Chameleon",
  "lineno": 12,
  "msecs": 354.42161560058594,
  "pathname": "/home/gladiatr/git/json-logs-for-kube/demo/efk/views.py",
  "process": 6800,
  "processName": "MainProcess",
  "relativeCreated": 41800.73118209839,
  "thread": 140275726399232,
  "threadName": "<concurrent.futures.thread.ThreadPoolExecutor object at 0x7f947f4b0828>_0",
  "levelname": "INFO",
  "x_node_name": "ip-10-70-59-190.eu-central-1.compute.internal",
  "x_sa_name": "default",
  "x_pod_ip": "100.96.1.11",
  "build": "5000",
  "builder": "Stephen Spencer",
  "image": "gladiatr72/kube-demo",
  "version": "1.0.2",
  "app": "kube-demo",
  "env": "dev",
  "pod-template-hash": "2802633501",
  "something": "else",
  "additional data": "whee"
}
{
  "asctime": "2017-07-12 21:08:16,369",
  "message": "(access record)",
  "name": "gunicorn.access",
  "created": 1499893696.3695881,
  "filename": "glogging.py",
  "module": "glogging",
  "funcName": "access",
  "lineno": 327,
  "msecs": 369.58813667297363,
  "pathname": "/home/gladiatr/.virtualenvs/json-logs-for-kube/lib/python3.6/site-packages/gunicorn/glogging.py",
  "process": 6800,
  "processName": "MainProcess",
  "relativeCreated": 41815.89770317078,
  "thread": 140275726399232,
  "threadName": "<concurrent.futures.thread.ThreadPoolExecutor object at 0x7f947f4b0828>_0",
  "levelname": "INFO",
  "x_node_name": "ip-10-70-59-190.eu-central-1.compute.internal",
  "x_sa_name": "default",
  "x_pod_ip": "100.96.1.11",
  "build": "5000",
  "builder": "Stephen Spencer",
  "image": "gladiatr72/kube-demo",
  "version": "1.0.2",
  "app": "kube-demo",
  "env": "dev",
  "pod-template-hash": "2802633501",
  "something": "else",
  "access": {
    "remote": "10.0.1.195",
    "method": "GET",
    "url-path": "/",
    "query": "",
    "username": "-",
    "protocol": "HTTP/1.0",
    "status": "200",
    "response-length": "140",
    "referrer": "-",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "request-time": "0.019269"
  }
}
```


## Example Kubernetes deployment:

```yaml

apiVersion: extensions/v1beta1
kind: Deployment
metadata:         <<-- This is not the metadata you are looking for
  name: kube-demo
  labels:
    project: kube-demo
    environment: dev
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kube-demo
      env: dev
  template:
    metadata:
      labels:
        app: kube-demo
        env: dev
        something: else
      annotations:
        build: "5000"
        builder: "Stephen Spencer"
        image: "gladiatr72/kube-demo"
        version: "1.0.2"

```

### Currently only `metadata.(labels|annotations)` are supported for exposure via volume.
(_Reasons_, right?)


```yaml
    spec:
      volumes:
          name: podinfo
          downwardAPI:
            items:
              - path: labels
                fieldRef:
                  fieldPath: metadata.labels
              - path: annotations
                fieldRef:
                  fieldPath: metadata.annotations
      containers:
        - name: kube-demo
          image: gladiatr72/kube-demo:1.0.2
          volumeMounts:
            -
              name: run
              mountPath: /run
            -
              name: podinfo
              readOnly: true
              mountPath: /etc/meta  <<-- KUBE_META must equal this
```

### environment variable prefixes
(or: how to avoid looking like a complete idiot when you spam your data-store
password into your logging system)

You can use whatever letter or sequence for the prefix as long as it gets matched
with the value of `KUBE_META_ENV_PREFIX`.

```yaml
          env:
            - name: MEMCACHE_HOST
              value: unix:/run/memcache.sock
            - name: DJANGO_SETTINGS_MODULE
              value: "revsys.settings.dev"
            - name: DJANGO_FQDN
              value: kube-demo.dev.revsys.com
            - name: *X_NODE_NAME
              valueFrom:
                fieldRef:
                 fieldPath: spec.nodeName
            - name: *X_POD_IP
              valueFrom:
                fieldRef:
                  fieldPath: status.podIP
            - name: *X_SA_NAME
              valueFrom:
                fieldRef:
                  fieldPath: spec.serviceAccountName
            - name: REDIS_PASSWORD  (oh, nos!)
              valueFrom:
                secretKeyRef:
                  name: redis
                  key: pass
          ports:
            - containerPort: 8000

    * unmagical prefix set in KUBE_META_ENV_PREFIX

```

## The logging configuration

It’s just a standard python dictionary. The most obvious thing to change
is the handler definition.


```python

from jslog4kube import LOGGING

LOGGING_HANDLERS = {
    'mypackage': {
        'handlers': ['json-stdout'],
        'formatters': ['json'],
        'propagate’: False,
        'level’: 'ERROR',
    }
}

LOGGING['handlers'].update(LOGGING_HANDLERS)

```

## Setup your python/django apps to log correctly

The `LOGGING` dict this provides sets up the "general" things to log, but if
you want to include your own Python libraries or Django apps you need to specify
them.  To specify a Django app named 'foo', you would simply adjust the `LOGGING` dict like this:

```
LOGGERS = {
    'foo': {
        'handlers': ['json-stdout'],
        'formatters': ['json'],
        'propagate': True,
        'level': 'INFO',
    }
}

LOGGING['loggers'].update(LOGGERS)

dictConfig(LOGGING)
```

Or if you want to log EVERYTHING at an `DEBUG` level you can set a blank (aka default) logger:

```
LOGGERS = {
    '': {
        'handlers': ['json-stdout'],
        'formatters': ['json'],
        'propagate': True,
        'level': 'DEBUG',
    }
}

LOGGING['loggers'].update(LOGGERS)

dictConfig(LOGGING)
```

## Usage

This is normal Python logging so you can do something simple like our info call
below or more complex like the debug call and add additional data to the log information:

```
import logging

logger = logging.getLogger(__name__)

logger.info("Simple log message")

foo = 12
bar = 'something else'
logger.debug("More complicated message", extra={
  "foo": foo,
  "bar": bar,
})

```

## Need help?

[REVSYS](http://www.revsys.com?utm_medium=github&utm_source=jslog4kube) can help with your Python, Django, and infrastructure projects. If you have a question about this project, please open a GitHub issue. If you love us and want to keep track of our goings-on, here's where you can find us online:

<a href="https://revsys.com?utm_medium=github&utm_source=jslog4kube"><img src="https://pbs.twimg.com/profile_images/915928618840285185/sUdRGIn1_400x400.jpg" height="50" /></a>
<a href="https://twitter.com/revsys"><img src="https://cdn1.iconfinder.com/data/icons/new_twitter_icon/256/bird_twitter_new_simple.png" height="43" /></a>
<a href="https://www.facebook.com/revsysllc/"><img src="https://cdn3.iconfinder.com/data/icons/picons-social/57/06-facebook-512.png" height="50" /></a>
