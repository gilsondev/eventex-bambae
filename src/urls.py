# -*- coding: utf8 -*-

from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('src',
    url(r'^$', 'core.views.home', name='homepage'),
    url(r'^inscricao/', include('src.subscriptions.urls',
                                namespace='subscriptions')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
