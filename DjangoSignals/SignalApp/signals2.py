from django.dispatch import receiver, Signal

# custom signal
pre_contact_added_signal = Signal(providing_args=['contact'])

@receiver(pre_contact_added_signal)
def pre_save_receiver1(sender, **kwargs):
        with open('log1.txt', 'a') as f:
                f.write(str(kwargs['contact'])+'\n')


@receiver(pre_contact_added_signal)
def pre_save_receiver2(sender, **kwargs):
    with open('log2.txt', 'a') as f:
        f.write(str(kwargs['contact'])+'\n')