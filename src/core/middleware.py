# -*- coding: utf8 -*-
from django.conf import settings
from django.views.debug import cleanse_setting, CLEANSED_SUBSTITUTE


def cleanse_envvar(key, value):
    hidden_envvars = getattr(settings, 'HIDDEN_ENVVARS', [])
    if key in hidden_envvars:
        return CLEANSED_SUBSTITUTE
    else:
        return cleanse_setting(key, value)


class HiddenEnvVarsMiddleware(object):
    """Classe responsável por retirar variáveis de ambiente
    que exibem informações de risco do projeto.

    É necessário inserir a variável a ser alterada em ``HIDDEN_ENVVARS``
    no arquivo ``settings.py``. Exemplo::

        HIDDEN_ENVVARS = [
            'DATABASE_PASSWORD',
            'EMAIL_PASSWORD',
        ]
    """
    def process_exception(self, request, exception):
        for key, value in request.META.items():
            request.META[key] = cleanse_envvar(key, value)
        return request
