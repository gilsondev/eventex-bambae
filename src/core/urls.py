# -*- coding: utf8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('src.core.views',
    url(r'^palestrantes/(?P<slug>[\w-]+)/$', 'speaker_detail',
        name='speaker_detail'),
)
