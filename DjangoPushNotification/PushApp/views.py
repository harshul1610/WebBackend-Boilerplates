# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.views.generic import TemplateView
from django.shortcuts import render, HttpResponse
from django.http.response import JsonResponse
from django.conf import settings
from django.forms.models import model_to_dict
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from .forms import SubscriptionInformationform, WebPushForm
from django.contrib.auth.models import User
from pywebpush import WebPushException, webpush


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
            user, created = User.objects.get_or_create(username='Anonymous')
            
            subscription = sub_form.get_or_save()
            web_push_data = web_push_form.cleaned_data
            # get the status type
            status_type = web_push_data.pop('status_type')
            # save or delete the information based on status
            web_push_form.save_or_delete(subscription=subscription , user=user, status_type=status_type)
            # return the http status response accordingly.
            if status_type == 'unsubscribe':
                return HttpResponse(status=202)
            elif status_type == 'subscribe':
                return HttpResponse(status=201)
    return HttpResponse(status=400)

def SendNotification(request):
    try:
        user_obj = request.user
        if not request.user.is_authenticated():
            user_obj = User.objects.get(username='Anonymous')

        pushinfo_objs = user_obj.pushinfo.select_related("subscription")

        errors = []
        for pushinfo_obj in pushinfo_objs:
            try:
                subscription_data = model_to_dict(pushinfo_obj.subscription, exclude=['browser', 'id'])
                print subscription_data
                endpoint = subscription_data['endpoint']
                p256dh = subscription_data['p256dh']
                auth = subscription_data['auth']

                final_subscription_data = {
                    'endpoint': endpoint,
                    'keys': {'auth': auth, 'p256dh': p256dh}
                }

                vapid_data = {}

                vapid_settings = getattr(settings, 'VAPID_SETTINGS', {})
                vapid_private_key = vapid_settings.get('VAPID_PRIVATE_KEY')
                vapid_admin_email = vapid_settings.get('VAPID_ADMIN_EMAIL')

                if vapid_private_key:
                    vapid_data = {
                        'vapid_private_key': vapid_private_key,
                        'vapid_claims': {"sub": "mailto:{}".format(vapid_admin_email)}
                    }
                payload = {'head': 'Web Push Example', 'body': 'Hell Yeah! Notification Works!'}

                req = webpush(subscription_info=final_subscription_data, data=json.dumps(payload), ttl=0, **vapid_data)

            except WebPushException as ex:
                errors.append(dict(subscription=pushinfo_obj.subscription,
                                exception=ex))
        if errors:
            raise WebPushException("Push failed.", extra=errors)
        return JsonResponse(status=200, data={"message": "Web push successful"})
    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occurred"})
