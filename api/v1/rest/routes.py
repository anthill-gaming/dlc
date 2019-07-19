# For more details about routing, see
# http://www.tornadoweb.org/en/stable/routing.html
from tornado.web import url
from . import handlers

route_patterns = [
    url(r'^/bundle/(?P<id>[^/]+)/?$', handlers.BundleHandler, name='bundle'),
    url(r'^/bundle/?$', handlers.BundleHandler, name='bundle_create'),
    url(r'^/data/(?P<app_name>[^/]+)/(?P<app_version>[^/]+)/?$',
        handlers.BundlesHandler, name='bundles'),
]
