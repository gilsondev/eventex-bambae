# -*- coding: utf8 -*-
from django import forms
from django.utils.translation import ugettext as _

from .models import Subscription


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        exclude = ('paid',)

    def clean(self):
        super(SubscriptionForm, self).clean()

        if not self.cleaned_data.get('email') and \
           not self.cleaned_data.get('phone'):
            raise forms.ValidationError(
                _(u'Informe seu e-mail ou telefone.'))
        return self.cleaned_data

    def _unique_check(self, fieldname, error_message):
        param = {fieldname: self.cleaned_data[fieldname]}
        if Subscription.objects.filter(**param).exists():
            raise forms.ValidationError(error_message)
        return self.cleaned_data[fieldname]
