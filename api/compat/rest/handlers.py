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
    """
    Multiple operations with bundles:
        fetching, creating, updating and deleting.
    """
    model = Bundle
    form_class = BundleForm

    def get_form_class(self):
        """Return the form class to use in this handler."""
        form_class = super().get_form_class()
        if self.request.method in ('PUT',):  # Updating
            # Patching form meta
            class Meta(form_class.Meta):
                all_fields_optional = True
                assign_required = False

            form_class.Meta = Meta
        return form_class
