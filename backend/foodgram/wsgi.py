"""
Конфигурация WSGI для проекта Foodgram.
WSGI configuration for the Foodgram project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodgram.settings')

application = get_wsgi_application()
