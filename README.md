
# jslog4kube (python/JSON logging for kubernetes pod/containers)


## Why?

  * provide a JSON-to-stdout setup for python
  * provide the same JSON-to-stdout setup for [gunicorn](http://gunicorn.org)
  * because creating complex log collector configs to handle whatever
    that other person thought was a good-idea-at-the-time is for the birds.

### making it go

Two environment variables configure this module:

    * `KUBE_META`: specifies the mount-point for the Kubernetes downward-API [volumes](https://kubernetes.io/docs/tasks/inject-data-application/downward-api-volume-expose-pod-information/) bits (default: /etc/meta)

    * `KUBE_META_ENV_PREFIX`: the textual prefix for any [environment variables](https://kubernetes.io/docs/tasks/inject-data-application/environment-variable-expose-pod-information/) targetted for inclusion in this pod’s log records (default: X) 


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
  "asctime": "2017-07-12 13:28:11,945",
  "message": "Starting gunicorn 19.7.1",
  "name": "gunicorn.error",
  "created": 1499884091.9452283,
  "filename": "glogging.py",
  "module": "glogging",
  "funcName": "info",
  "lineno": 247,
  "msecs": 945.2283382415771,
  "pathname": "/home/gladiatr/.virtualenvs/wharton-kube/lib/python3.6/site-packages/gunicorn/glogging.py",
  "process": 58369,
  "processName": "MainProcess",
  "relativeCreated": 75.57559013366699,
  "thread": 140118305551424,
  "threadName": "MainThread",
  "levelname": "INFO",
  "x_node_name": "ip-10-70-59-190.eu-central-1.compute.internal",
  "x_sa_name": "default",
  "x_pod_ip": "100.96.1.11"
}
{
  "asctime": "2017-07-12 18:33:39,068",
  "message": "(access record)",
  "name": "gunicorn.access",
  "created": 1499884419.0684257,
  "filename": "glogging.py",
  "module": "glogging",
  "funcName": "access",
  "lineno": 327,
  "msecs": 68.42565536499023,
  "pathname": "/home/gladiatr/.virtualenvs/wharton-kube/lib/python3.6/site-packages/gunicorn/glogging.py",
  "process": 60150,
  "processName": "MainProcess",
  "relativeCreated": 55312.14499473572,
  "thread": 140701128676416,
  "threadName": "MainThread",
  "levelname": "INFO",
  "x_node_name": "ip-10-70-59-190.eu-central-1.compute.internal",
  "x_sa_name": "default",
  "x_pod_ip": "100.96.1.11",
  "access": {
    "remote": "10.0.1.195",
    "method": "GET",
    "url-path": "/",
    "query": "a=1&b=2",
    "username": "-",
    "protocol": "HTTP/1.0",
    "status": "200",
    "response-length": "218",
    "referrer": "-",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0",
    "request-time": "0.047402"
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

### Currently only `metadata.(labels|annotations)` are supported for exposure via
volume. (_Reasons_, right?)

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
is the handler definitions.


```python

from jslog4kube import LOGGING

LOGGING_HANDLERS = {
    ‘mypackage’: {
        ‘handlers’: [‘json-stdout’],
        ‘formatters’: [‘json’],
        ‘propagate’: False,
        ‘level’: ERROR,
    }
}

LOGGING[‘handlers’].update(LOGGING_HANDLERS)

```





