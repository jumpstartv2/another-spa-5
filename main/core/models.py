from __future__ import unicode_literals

from django.db import models
from django.forms.models import model_to_dict
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class ModelDiffMixin(object):
    """
    A model mixin that tracks model fields' values and provide some useful api
    to know what fields have been changed.
    """

    def __init__(self, *args, **kwargs):
        super(ModelDiffMixin, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(ModelDiffMixin, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in self._meta.fields])


class AbstractTimeStampedModel(models.Model, ModelDiffMixin):
    """
    Base for time-stamped models.
    """

    created_at = models.DateTimeField(_('Created At'), editable=False)
    updated_at = models.DateTimeField(_('Updated At'), editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # check if the instace already has an id
        if not self.created_at:
            self.created_at = timezone.now()

        # update date modified
        self.updated_at = timezone.now()

        return super(AbstractTimeStampedModel, self).save(*args, **kwargs)
