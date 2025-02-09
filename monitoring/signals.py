# monitoring/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Farmer


@receiver(post_save, sender=CustomUser)
def create_farmer_profile(sender, instance, created, **kwargs):
    if created and not instance.is_staff and not instance.is_superuser:
        # Check for existing farmer first
        Farmer.objects.get_or_create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_farmer_profile(sender, instance, **kwargs):    
    if hasattr(instance, 'farmer'):
        instance.farmer.save()
