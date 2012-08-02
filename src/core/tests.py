# -*- coding: utf8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Speaker, Contact, Talk


class HomepageTest(TestCase):
    def test_get_homepage(self):
        response = self.client.get('/')
        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'index.html')


class SpeakerModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker(
            name="Henrique Bastos",
            slug="henrique-bastos",
            url="http://henriquebastos.net",
            description="Passionate software developer",
            avatar="")
        self.speaker.save()

    def test_create(self):
        self.assertEquals(1, self.speaker.pk)

    def test_unicode(self):
        self.assertEquals("Henrique Bastos", unicode(self.speaker))


class SpeakerDetailTest(TestCase):
    def setUp(self):
        Speaker.objects.create(name="Henrique Bastos",
                               slug="henrique-bastos",
                               url="http://henriquebastos.net",
                               description="Passionate software developer!",
                               avatar="")
        self.resp = self.client.get(reverse('core:speaker_detail',
                                            kwargs={'slug': 'henrique-bastos'}))

    def test_get(self):
        'Ao acessar os detalhes deve retornar com status 200'
        self.assertEquals(200, self.resp.status_code)

    def test_use_template(self):
        'Na requisição, deve enviar na resposta o template correto renderizado'
        self.assertTemplateUsed(self.resp, 'core/speaker_detail.html')

    def test_speaker_in_context(self):
        'O palestrante requisitado deve estar no contexto da view'
        self.assertIsInstance(self.resp.context['speaker'], Speaker)


class ContactModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
            name="Henrique Bastos",
            url="http://henriquebastos.net",
            avatar="",
            description="Passionate software developer!")

    def test_create_email(self):
        contact = Contact.objects.create(speaker=self.speaker, kind='E',
                                         value="henrique@bastos.net")
        self.assertEquals(1, contact.pk)
