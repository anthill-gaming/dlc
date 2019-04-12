# For more details about routing, see
# http://www.tornadoweb.org/en/stable/routing.html
from tornado.web import url
from . import handlers

route_patterns = [
    url(r'/bundle/(?P<bundle_id>\d*)/?', handlers.BundleHandler, name='bundle'),
    url(r'/data/(?P<app_name>[a-z0-9_-]+)/(?P<app_version>[a-z0-9_\.-]+)/?',
        handlers.BundlesHandler, name='bundles')
]
