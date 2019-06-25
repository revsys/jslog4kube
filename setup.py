import os

from setuptools import setup

BASE_DIR = os.path.dirname(__file__)

with open(os.path.join(BASE_DIR, "README.md")) as f:
    long_description = f.read()

setup(
    name="jslog4kube",
    version="1.0.6",
    description="relatively hassle-free JSON logging for Kubernetes pods",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://gitlab.com/stephen6/jslog4kube",
    author="Stephen D. Spencer",
    author_email="stephen@revsys.com",
    license="MIT",
    packages=["jslog4kube", "jslog4kube.kube", "jslog4kube.gunicorn"],
    install_requires=["python-json-logger"],
    zip_safe=False,
)
