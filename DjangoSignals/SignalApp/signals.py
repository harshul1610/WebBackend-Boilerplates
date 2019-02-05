from django.dispatch import receiver
from django.db.models.signals import post_save
from SignalApp.models import Contact


# prebuilt signal
@receiver(post_save, sender=Contact)
def post_save_receiver(sender, instance, **kwargs):
    with open('log.txt', 'a') as f:
        f.write(str(instance)+'\n')