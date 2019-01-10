from django import forms
from .models import SubscriptionInformation, PushInformation

class SubscriptionInformationform(forms.ModelForm):
    class Meta:
        model = SubscriptionInformation
        fields = ('browser', 'endpoint', 'auth', 'p256dh')

    def get_or_save(self):
        subscription_obj, created = SubscriptionInformation.objects.get_or_create(**self.cleaned_data)
        return subscription_obj

class WebPushForm(forms.Form):
    status_type = forms.ChoiceField(choices=[
                                      ('subscribe', 'subscribe'),
                                      ('unsubscribe', 'unsubscribe')
                                    ])
    
    def save_or_delete(self, subscription, user, status_type):
        data = {}
        data['user'] = user
        data['subscription'] = subscription
        push_obj, created = PushInformation.objects.get_or_create(**data)
        if status_type == 'unsubscribe':
            push_obj.delete()
            subscription.delete()