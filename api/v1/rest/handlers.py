from anthill.platform.api.rest.handlers.detail import DetailMixin
from anthill.platform.api.rest.handlers.list import ListHandler
from anthill.platform.api.rest.handlers.edit import (
    CreatingMixin, UpdatingMixin, DeletionMixin, ModelFormHandler)
from dlc.models import Bundle
from .forms import BundleForm


class BundlesHandler(ListHandler):
    """Get list of bundles."""
    model = Bundle


class BundleHandler(CreatingMixin, UpdatingMixin, DeletionMixin, DetailMixin,
                    ModelFormHandler):
    """Multiple operations with bundles."""
    model = Bundle
    form_class = BundleForm
