#!/usr/bin/eval PYTHON_VERSION=2.6 DJANGO_VERSION=1.6 PYTHONPATH=/home/pabluk/www/profilitique.debugstack.com/commons/modules python
import os, sys

_PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _PROJECT_DIR)
sys.path.insert(0, os.path.dirname(_PROJECT_DIR))


_PROJECT_NAME = 'profilitique'

os.environ['DJANGO_SETTINGS_MODULE'] = "%s.settings" % _PROJECT_NAME

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")

