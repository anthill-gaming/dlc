from anthill.framework.forms.orm import (
    ModelForm, ModelUpdateForm, ModelCreateForm, ModelSearchForm)
from dlc.models import Bundle


class BundleForm(ModelForm):
    class Meta:
        model = Bundle
