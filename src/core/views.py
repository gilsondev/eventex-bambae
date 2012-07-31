# -*- coding: utf8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext


def home(request):
    context = RequestContext(request)
    return render_to_response('index.html', context)
