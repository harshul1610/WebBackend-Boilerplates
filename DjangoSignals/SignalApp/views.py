# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from .forms import ContactForm


# Create your views here.
def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print 'saving the form'
            form.save()
    else:
        form = ContactForm()
    return render(request, 'home.html', context={'form':form})