# -*- coding: utf8 -*-
from django.test import TestCase

from .models import Speaker


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
