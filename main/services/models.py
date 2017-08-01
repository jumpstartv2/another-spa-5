from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import AbstractTimeStampedModel


optional = {
    'blank': True,
    'null': True,
}


class Service(AbstractTimeStampedModel):
    name = models.CharField(_('Name'), max_length=65)
    identifier = models.CharField(_('Identifier'), max_length=50)
    settings = models.ManyToManyField('services.Setting', related_name='settings', verbose_name=_('Settings'))
    
    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def __str__(self):
        return self.name


class Setting(AbstractTimeStampedModel):
    TYPE_ACCESS_TOKEN = 0
    TYPE_USERNAME = 1
    TYPE_PASSWORD = 2
    TYPE_API_URL = 3
    TYPE_KEY = 4
    TYPE_SECRET = 5
    IDENTIFIER_CHOICES = (
        (TYPE_ACCESS_TOKEN, 'Access Token'),
        (TYPE_USERNAME, 'Username'),
        (TYPE_PASSWORD, 'Password'),
        (TYPE_API_URL, 'API Url'),
        (TYPE_KEY, 'Key'),
        (TYPE_SECRET, 'Secret'),
    )
    
    name = models.CharField(_('Name'), max_length=65)
    identifier = models.IntegerField(_('Identifier'), choices=IDENTIFIER_CHOICES, default=TYPE_ACCESS_TOKEN)
    value = models.TextField(_('Value'))
    
    class Meta:
        verbose_name = _('Setting')
        verbose_name_plural = _('Settings')

    def __str__(self):
        return self.name
