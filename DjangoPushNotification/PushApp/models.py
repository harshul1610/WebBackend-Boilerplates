# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.db import models
from django.conf import settings

# Create your models here.
class SubscriptionInformation(models.Model):
    '''
    Model to Store the Subscription Information.
    '''
    browser = models.CharField(max_length=100)
    endpoint = models.URLField(max_length=255)
    auth = models.CharField(max_length=100)
    p256dh = models.CharField(max_length=100)


class PushInformation(models.Model):
    '''
    Model to build the relationship between User and SubscriptionInformation Model.
    '''
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='pushinfo', blank=True, null=True, on_delete=models.CASCADE)
    subscription = models.ForeignKey(SubscriptionInformation, related_name='pushinfo', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.user:
            super(PushInformation, self).save(*args, **kwargs)
        else:
            raise FieldError('User is not present.')