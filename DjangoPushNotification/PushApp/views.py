# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.views.generic import TemplateView
from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from .forms import SubscriptionInformationform, WebPushForm
from django.contrib.auth.models import User


# Create your views here.
@require_GET
def home(request):
    vapid_settings = getattr(settings, 'VAPID_SETTINGS', {})
    vapid_key = vapid_settings.get('VAPID_PUBLIC_KEY')
    user = request.user
    return render(request, 'home.html', context={'user': user, 'vapid_key':vapid_key})

class ServiceWorkerView(TemplateView):
    template_name = 'serviceworker.js'
    content_type = 'application/javascript'

@require_POST
@csrf_exempt
def SaveInformation(request):
    try:
        # get the request data
        request_post_data = json.loads(request.body.decode('utf-8'))
        print(request_post_data)
    except ValueError:
        return HttpResponse(status=400)
    
    new_subscription_data = {}
    subscription_data = request_post_data['subscription']

    # parse the subscription data
    new_subscription_data['browser'] = request_post_data['browser']
    new_subscription_data['endpoint'] = subscription_data['endpoint']
    new_subscription_data['auth'] = subscription_data['keys']['auth']
    new_subscription_data['p256dh'] = subscription_data['keys']['p256dh']
    # get the subscription form object from the form data.
    sub_form = SubscriptionInformationform(new_subscription_data)
    # get the web push form objection from all the data.
    web_push_form = WebPushForm(request_post_data)

    if sub_form.is_valid() and web_push_form.is_valid():
        # If user is present save the subscription info in the subscriptioninformation model.
        if request.user.is_authenticated():
            subscription = sub_form.get_or_save()
            web_push_data = web_push_form.cleaned_data
            # get the status type
            status_type = web_push_data.pop('status_type')
            # save or delete the information based on status
            web_push_form.save_or_delete(subscription=subscription , user=request.user, status_type=status_type)
            # return the http status response accordingly.
            if status_type == 'unsubscribe':
                return HttpResponse(status=202)
            elif status_type == 'subscribe':
                return HttpResponse(status=201)
        else:
            anonymous_user = User(username='Anonymous')
            anonymous_user.save()

            subscription = sub_form.get_or_save()
            web_push_data = web_push_form.cleaned_data
            # get the status type
            status_type = web_push_data.pop('status_type')
            # save or delete the information based on status
            web_push_form.save_or_delete(subscription=subscription , user=anonymous_user, status_type=status_type)
            # return the http status response accordingly.
            if status_type == 'unsubscribe':
                return HttpResponse(status=202)
            elif status_type == 'subscribe':
                return HttpResponse(status=201)
    return HttpResponse(status=400)

def SendNotification(request):
    pass