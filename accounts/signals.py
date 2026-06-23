# We don’t want to manually create Profile every time a user registers.
# So Django automatically creates it using signals

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # avoids duplicate entries
        Profile.objects.create(user=instance)