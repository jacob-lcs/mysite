"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""
import os,sys
sys.path.append(r"/home/ubuntu/.local/lib/python3.5/site-packages")
print(os.listdir("/home/ubuntu/.local/lib/python3.5/site-packages"))
print(sys.path)
from os.path import join, dirname, abspath
import django
from django.core.wsgi import get_wsgi_application
import sys  # 4

PROJECT_DIR = dirname(dirname(abspath(__file__)))  # 3

sys.path.insert(0, PROJECT_DIR)  # 5

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = get_wsgi_application()

