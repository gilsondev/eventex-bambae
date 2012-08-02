# -*- coding: utf8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Speaker(models.Model):
    name = models.CharField(_(u'Nome'), max_length=255)
    slug = models.SlugField(_(u'Slug'))
    url = models.URLField(_(u'Url'))
    description = models.TextField(_(u'Descrição'), blank=True)
    avatar = models.FileField(_(u'Avatar'),
                              upload_to='palestrantes',
                              blank=True, null=True)

    def __unicode__(self):
        return self.name
