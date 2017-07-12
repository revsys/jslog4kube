
from setuptools import setup

setup(name='jslog4kube',
      version='1.0.0',
      description='relatively hassle-free JSON logging for Kubernetes pods',
      url='http://gitlab.com/stephen6/jslog4kube',
      author='Stephen D. Spencer',
      author_email='stephen@revsys.com',
      license='MIT',
      packages=['jslog4kube'],
      install_requires=[
          'python-json-logger',
      ],
      zip_safe=False)
