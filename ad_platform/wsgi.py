# ad_platform/ad_platform/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ad_platform.settings')
application = get_wsgi_application()
