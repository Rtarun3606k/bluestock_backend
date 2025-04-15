import uuid
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create UserProfile when a new User is created
    """
    if created:
        # Generate a unique API key for the user
        api_key = uuid.uuid4().hex
        UserProfile.objects.create(user=instance, api_key=api_key)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to save UserProfile when User is saved
    """
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        # Create a profile if it doesn't exist
        api_key = uuid.uuid4().hex
        UserProfile.objects.create(user=instance, api_key=api_key)