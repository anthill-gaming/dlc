from anthill.framework.conf import settings
from anthill.framework.utils.http_client import upload
from anthill.framework.utils.module_loading import import_string
from anthill.framework.utils.urls import build_absolute_uri
from anthill.framework.utils.asynchronous import as_future
from anthill.framework.core.exceptions import ImproperlyConfigured
from anthill.framework.core.files.storage import default_storage
from anthill.framework.core.files.backends.sftpstorage import SFTPStorage
from anthill.platform.api.internal import InternalAPIMixin
from anthill.platform.utils.ssh import PrivateSSHKeyContext
from tornado.ioloop import IOLoop
from dlc.exceptions import DeploymentError

METHODS = getattr(settings, 'DEPLOYMENT_METHODS', [])


class DeploymentMethod(InternalAPIMixin):
    name = None

    def __init__(self):
        if self.name is None:
            raise ImproperlyConfigured('Deployment method name is required')

    @property
    def app(self):
        from anthill.framework.apps import app
        return app

    async def deploy(self, src: str, dst: str) -> str:
        raise NotImplementedError(
            'subclasses of DeploymentMethod must provide a deploy() method')

    def url(self, path: str) -> str:
        raise NotImplementedError(
            'subclasses of DeploymentMethod must provide a url() method')

    def configure(self, **kwargs):
        raise NotImplementedError(
            'subclasses of DeploymentMethod must provide a configure() method')


class LocalDeploymentMethod(DeploymentMethod):
    """Stores files on local filesystem."""

    name = 'local'

    def __init__(self):
        super().__init__()
        self.base_url = settings.LOCATION

    @as_future
    def deploy(self, src: str, dst: str) -> str:
        with open(src, 'rb') as src_f:
            default_storage.save(dst, src_f)
        return self.url(dst)

    def url(self, path: str) -> str:
        path = default_storage.url(path)
        return build_absolute_uri(self.base_url, path)

    def configure(self, **kwargs):
        pass


class MediaDeploymentMethod(DeploymentMethod):
    """Stores files on anthill media server."""

    name = 'media'

    def __init__(self):
        super().__init__()
        self.upload_url = None
        IOLoop.current().add_callback(self.set_upload_url)

    async def set_upload_url(self):
        self.upload_url = await self.internal_request('media', 'get_upload_url')

    async def deploy(self, src: str, dst: str) -> str:
        await upload([src], self.upload_url)
        return self.url(dst)

    def url(self, path: str) -> str:
        return build_absolute_uri(self.upload_url, path)

    def configure(self, **kwargs):
        pass


class KeyCDNDeploymentMethod(DeploymentMethod):
    """Stores files on KeyCDN servers."""

    name = 'keycdn'
    hostname = 'rsync.keycdn.com'

    def __init__(self, username=None, zone=None, key_data=None, base_url=None, root_path=None):
        super().__init__()
        self.username = username
        self.zone = zone
        self.key_data = key_data
        self.base_url = base_url
        self.root_path = root_path

    def configure(self, username=None, zone=None, key_data=None, base_url=None, root_path=None):
        self.username = username
        self.zone = zone  # TODO:
        self.key_data = key_data
        self.base_url = base_url
        self.root_path = root_path

    @as_future
    def deploy(self, src: str, dst: str) -> str:
        with PrivateSSHKeyContext(self.key_data) as key_filename:
            kwargs = {
                'host': self.hostname,
                'username': self.username,
                'root_path': self.root_path,
                'params': {
                    'key_filename': key_filename,
                    'compress': False,
                },
                'file_mode': settings.FILE_UPLOAD_PERMISSIONS,
                'dir_mode': settings.FILE_UPLOAD_DIRECTORY_PERMISSIONS,
            }
            storage = SFTPStorage(**kwargs)
            with open(src, 'rb') as src_f:
                storage.save(dst, src_f)

            return self.url(dst)

    def url(self, path: str) -> str:
        return build_absolute_uri(self.base_url, path)


class Deployment:
    """Deployment methods switching class."""

    methods = METHODS

    @property
    def _methods(self):
        return (import_string(m) for m in self.methods)

    @property
    def methods_dict(self):
        return {m.name: m for m in self._methods}

    def get_method(self, name):
        try:
            return self.methods_dict[name]
        except KeyError:
            raise ValueError('Deployment method `%s` is not supported' % name)
