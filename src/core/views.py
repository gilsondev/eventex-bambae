# -*- coding: utf8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from .models import Speaker


def home(request):
    context = RequestContext(request)
    return render_to_response('index.html', context)


def speaker_detail(request, slug):
    speaker = get_object_or_404(Speaker, slug=slug)
    return render_to_response('core/speaker_detail.html', {
        'speaker': speaker
    })
