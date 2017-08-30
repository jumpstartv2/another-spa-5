from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import AbstractTimeStampedModel


optional = {
    'blank': True,
    'null': True,
}


class Service(AbstractTimeStampedModel):
    TYPE_GITHUB = 0
    TYPE_BITBUCKET = 1
    TYPE_JIRA = 2
    TYPE_ODOO = 3
    IDENTIFIER_CHOICES = (
        (TYPE_GITHUB, 'Github'),
        (TYPE_BITBUCKET, 'Bitbucket'),
        (TYPE_JIRA, 'Jira'),
        (TYPE_ODOO, 'Odoo'),
    )
    
    TYPE_REPO = 0
    TYPE_PM = 1
    SERVICE_TYPE_CHOICES = (
        (TYPE_REPO, 'repository'),
        (TYPE_PM, 'pm_tool'),
    )
    
    name = models.CharField(_('Name'), max_length=65)
    identifier = models.IntegerField(_('Identifier'), choices=IDENTIFIER_CHOICES, default=TYPE_GITHUB)
    service_type = models.IntegerField(_('Service Type'), choices=SERVICE_TYPE_CHOICES, default=TYPE_REPO)
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
    TYPE_DATABASE_NAME = 6
    TYPE_PM = 7
    IDENTIFIER_CHOICES = (
        (TYPE_ACCESS_TOKEN, 'access_token'),
        (TYPE_USERNAME, 'username'),
        (TYPE_PASSWORD, 'password'),
        (TYPE_API_URL, 'api_url'),
        (TYPE_KEY, 'key'),
        (TYPE_SECRET, 'secret'),
        (TYPE_DATABASE_NAME, 'database_name'),
        (TYPE_PM, 'pm'),
    )
    
    name = models.CharField(_('Name'), max_length=65)
    identifier = models.IntegerField(_('Identifier'), choices=IDENTIFIER_CHOICES, default=TYPE_ACCESS_TOKEN)
    value = models.TextField(_('Value'))
    
    class Meta:
        verbose_name = _('Setting')
        verbose_name_plural = _('Settings')

    def __str__(self):
        return self.name


class Template(AbstractTimeStampedModel):
    TYPE_DJANGO = 0
    TYPE_DJANGOREST = 1
    TYPE_IOS = 2
    TYPE_ANDROID = 3
    TYPE_SPA = 4
    TYPE_ECOMMERCE = 5
    TEMPLATE_CHOICES = (
        (TYPE_DJANGO, 'Django (Web)'),
        (TYPE_DJANGOREST, 'Django Rest'),
        (TYPE_IOS, 'iOS (Mobile)'),
        (TYPE_SPA, 'S.P.A.'),
        (TYPE_ECOMMERCE, 'E-Commerce'),
    )

    template_type = models.IntegerField(_('Template Type'), choices=TEMPLATE_CHOICES, default=TYPE_DJANGO)
    repo_url = models.TextField(_('Repo Url'))
    
    class Meta:
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')

    def __str__(self):
        return self.get_template_type_display()

