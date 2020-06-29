# Signals that fires when a user logs in and logs out

from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch import receiver

from CustomUser.models import LoggedInUser


# Signals that fires when a user logs in and logs out

@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    LoggedInUser.objects.get_or_create(logged_in_user=kwargs.get('user'))


@receiver(user_logged_out)
def on_user_logged_out(sender, **kwargs):
    LoggedInUser.objects.filter(logged_in_user=kwargs.get('user')).delete()
