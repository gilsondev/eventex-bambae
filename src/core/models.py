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


class KindContactManager(models.Manager):
    def __init__(self, kind):
        super(KindContactManager, self).__init__()
        self.kind = kind

    def get_query_set(self):
        qs = super(KindContactManager, self).get_query_set()
        qs = qs.filter(kind=self.kind)
        return qs


class Contact(models.Model):
    KINDS = (
        ('P', _(u'Telefone')),
        ('E', _(u'E-mail')),
        ('F', _(u'Fax')),
    )

    speaker = models.ForeignKey('Speaker', verbose_name=_(u'Palestrante'))
    kind = models.CharField(_(u'Tipo'), max_length=1, choices=KINDS)
    value = models.CharField(_(u'Valor'), max_length=255)

    objects = models.Manager()
    phones = KindContactManager('P')
    emails = KindContactManager('E')
    faxes = KindContactManager('F')
