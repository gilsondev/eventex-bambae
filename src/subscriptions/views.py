# -*- coding: utf8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.conf import settings

from .models import Subscription
from .forms import SubscriptionForm


def subscribe(request):
    if request.method == "POST":
        return create(request)
    else:
        return new(request)


def new(request):
    return direct_to_template(request,
        'subscriptions/subscription_form.html', {
        'form': SubscriptionForm()
    })


def create(request):
    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        template = 'subscriptions/subscription_form.html'
        return direct_to_template(request, template, {'form': form})

    subscription = form.save()
    send_mail(subject=u'Cadastrado com sucesso',
              message=u'Obrigado pela sua inscricao!',
              from_email=settings.DEFAULT_FROM_EMAIL,
              recipient_list=[subscription.email])

    return HttpResponseRedirect(reverse('subscriptions:success',
                                        args=[subscription.pk]))


def success(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk)

    template = 'subscriptions/subscription_detail.html'
    return direct_to_template(request, template, {'subscription': subscription})
