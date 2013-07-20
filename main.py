from beaker.middleware import SessionMiddleware
from google.appengine.dist import use_library 

use_library('django', '1.3')
import os,sys
#sys.path.append(sys.path.join(sys.path.dirname(__file__)))
sys.path.append(os.path.dirname(__file__))
#print sys.path.join(sys.path.dirname(__file__),'eventdemo')
#sys.path.append('/Users/xiafan/Documents/code/python/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'eventdemo.settings'

from django.conf import settings
settings._target = None

import django.core.handlers.wsgi

from google.appengine.ext.webapp import util
def main():
    # Run Django via WSGI.
    #print os.environ['DJANGO_SETTINGS_MODULE']
    application = django.core.handlers.wsgi.WSGIHandler()
    session_opts = {
        'session.type': 'ext:google',
        'session.cookie_expires': True,
        'session.auto': True,
        }
    application = SessionMiddleware(application, session_opts)
    util.run_wsgi_app(application)
def app():
    application = django.core.handlers.wsgi.WSGIHandler()
    session_opts = {
        'session.type': 'ext:google',
        'session.cookie_expires': True,
        'session.auto': True,
        }
    application = SessionMiddleware(application, session_opts)
    return application
application = app()
if __name__ == '__main__': 
    main()
