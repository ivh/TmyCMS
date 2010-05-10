import os
import sys
sys.path.append('/home/tom/py/')
sys.path.append('/home/tom/sites/')
sys.path.append('/home/tom/sites/MyDjangoSites')

os.environ['DJANGO_SETTINGS_MODULE'] = 'DjVAMDC.settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
