# For more details about routing, see
# http://www.tornadoweb.org/en/stable/routing.html
from tornado.web import url
from . import handlers as h


route_patterns = [
    url(r'^/bundle/(?P<id>[^/]+)/?$', h.BundleHandler, name='bundle'),
    url(r'^/bundle/?$', h.BundleHandler, name='bundle_create'),
    url(r'^/bundles/(?P<app_name>[^/]+)/(?P<app_version>[^/]+)/?$',
        h.BundlesHandler, name='bundles'),
]
