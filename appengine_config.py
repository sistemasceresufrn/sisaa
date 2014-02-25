from gaesessions import SessionMiddleware

# suggestion: generate your own random key using os.urandom(64)
# WARNING: Make sure you run os.urandom(64) OFFLINE and copy/paste the output to
# this file.  If you use os.urandom() to *dynamically* generate your key at
# runtime then any existing sessions will become junk every time you start,
# deploy, or update your app!
import os
COOKIE_KEY = '\xb1\x04\xf7\xc1k\xde\x1d\xef\x02v\xb1[\xf0o \xec\x1enh\xb9\xda\xb9\xc2\xcc\xe2$\xa8E\xbe\x7f\xa8\xc0(h\x1a`c/\x879l\x97\xf5\xf4\xb4\xa4\xe7\xfds\xcd\x8cy\x9b6\x8f\xa5ex\xe3\xa7\x0f\xc2\xb1\xc3'

def webapp_add_wsgi_middleware(app):
  from google.appengine.ext.appstats import recording
  app = SessionMiddleware(app, cookie_key=COOKIE_KEY)
  app = recording.appstats_wsgi_middleware(app)
  return app
