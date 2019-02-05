# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import RegexValidator
from SignalApp.signals2 import pre_contact_added_signal


# Create your models here.
class Contact(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format; '+999999999'. Upto 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    contact_name = models.CharField(max_length=50, blank=False)

    def __repr__(self):
        return "{}:{}".format(self.contact_name, self.phone_number)
    
    def __str__(self):
        return "{}:{}".format(self.contact_name, self.phone_number)
        
    def save(self, *args, **kwargs):
        pre_contact_added_signal.send(sender=Contact, contact = self)
        super(Contact, self).save(*args, **kwargs)

