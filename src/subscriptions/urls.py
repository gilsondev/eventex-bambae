# -*- coding: utf8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('src.subscriptions.views',
    url(r'^$', 'subscribe', name='subscribe'),
    url(r'^(\d+)/$', 'success', name='success'),
)
