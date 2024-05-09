"""Signals for user"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Profile, User


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Signals created profile for user."""
    if created:
        profile = Profile(user=instance)
        profile.save()
