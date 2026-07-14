from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Product, UserProfile

@receiver(post_save, sender=Product)
def update_user_profile(sender, instance, **kwargs):
    UserProfile.objects.filter(user = instance.seller).update(updated_at=timezone.now())


