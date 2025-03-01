from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserProgress

@receiver(post_save, sender=CustomUser)
def create_user_progress(sender, instance, created, **kwargs):
    if created:
        UserProgress.objects.create(user=instance)