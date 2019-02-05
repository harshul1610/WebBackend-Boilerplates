# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class SignalappConfig(AppConfig):
    name = 'SignalApp'

    def ready(self):
        import SignalApp.signals
        import SignalApp.signals2
