# -*- coding: utf8 -*-

from django.test import TestCase
from django.core.urlresolvers import reverse as r
from django.db import IntegrityError
from django.core import mail

from .models import Subscription
from .forms import SubscriptionForm


class SubscribeViewTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('subscriptions:subscribe'))

    def test_get(self):
        'Ao visitar /inscricao/ a página de inscrição é exibida'
        self.assertEquals(200, self.resp.status_code)

    def test_use_template(self):
        self.assertTemplateUsed(self.resp,
                                'subscriptions/subscription_form.html')

    def test_has_form(self):
        'A resposta deve contar o formulário de inscrição'
        self.assertIsInstance(self.resp.context['form'], SubscriptionForm)

    def test_form_has_fields(self):
        'O formulário deve conter campos: name, email, cpf e phone.'
        form = self.resp.context['form']
        self.assertItemsEqual(['name', 'email', 'cpf', 'phone'], form.fields)

    def test_html(self):
        'O html deve conter os campos do formulário'
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 4)
        self.assertContains(self.resp, 'type="submit"')


class SubscriptionModelTest(TestCase):
    def test_create(self):
        'O model deve ter: name, email, cpf, phone, created_at'
        s = Subscription.objects.create(
            name='Henrique Bastos',
            cpf='03901901981',
            email='henrique@bastos.net',
            phone='21-91820191',
        )
        self.assertEquals(s.id, 1)


class SubscriptionModelUniqueTest(TestCase):
    def setUp(self):
        # Cria uma primeira inscrição no banco
        Subscription.objects.create(name='Henrique Bastos', cpf='01234567890',
                                   email='henrique@bastos.net',
                                   phone='21-91811791')

    def test_cpf_must_be_unique(self):
        'CPF deve ser único'
        # instancia a inscrição do CPF existente
        s = Subscription(name='Henrique Bastos', cpf='01234567890',
                         email='outro@email.net', phone='21-91811791')

        # Verifica se ocorre o erro de integridade ao persistir.
        self.assertRaises(IntegrityError, s.save)

    def test_email_must_be_unique(self):
        'E-mail deve ser único'
        # instancia a inscrição do CPF existente
        s = Subscription(name='Henrique Bastos', cpf='000000000',
                         email='henrique@bastos.net', phone='21-91811791')

        # Verifica se ocorre o erro de integridade ao persistir.
        self.assertRaises(IntegrityError, s.save)


class SubscriptionViewPostTest(TestCase):
    def setUp(self):
        data = dict(name='Henrique Bastos', cpf='0000000000',
                   email='henrique@bastos.net', phone='21-0101-8173')
        self.resp = self.client.post(r('subscriptions:subscribe'), data)

    def test_redirect(self):
        'Post deve redirecionar para a página de sucesso'
        self.assertRedirects(self.resp, r('subscriptions:success', args=[1]))

    def test_save(self):
        'Post deve salvar Subscription o banco'
        self.assertTrue(Subscription.objects.exists())

    def test_email_sent(self):
        'Post deve notificar visitante por email.'
        self.assertEquals(1, len(mail.outbox))


class SubscriptionViewInvalidPostTest(TestCase):
    def setUp(self):
        data = dict(name='Henrique Bastos', cpf='000000000001',
                    email='henrique@bastos.net', phone='21-96186180')
        self.resp = self.client.post(r('subscriptions:subscribe'), data)

    def test_show_pages(self):
        'Post inválido não deve redirecionar'
        self.assertEquals(200, self.resp.status_code)

    def test_form_errors(self):
        'Form deve conter erros'
        self.assertTrue(self.resp.context['form'].errors)

    def test_must_not_save(self):
        'Dados não devem ser salvos.'
        self.assertFalse(Subscription.objects.exists())


class SuccessViewTest(TestCase):
    def setUp(self):
        s = Subscription.objects.create(name='Henrique Bastos', cpf='01234567890',
                                   email='henrique@bastos.net',
                                   phone='21-91811791')
        self.resp = self.client.get(r(
            'subscriptions:success', args=[s.pk]))

    def test_get(self):
        'Visita /inscricao/1/ e retorna 200.'
        self.assertEquals(200, self.resp.status_code)

    def test_template(self):
        'Renderiza o template'
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_detail.html')

    def test_context(self):
        'Verifica instância de subscription no contexto'
        subscription = self.resp.context['subscription']
        self.assertIsInstance(subscription, Subscription)

    def test_html(self):
        'Página deve conter nome do cadastrado.'
        self.assertContains(self.resp, 'Henrique Bastos')


class SuccessViewNotFound(TestCase):
    def test_not_found(self):
        'Acesso á inscrição não cadastrada deve retornar 404.'
        response = self.client.get(r('subscriptions:success', args=[0]))
        self.assertEquals(404, response.status_code)
