from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from logs.models import logs

@receiver(post_save, sender)
def create_user_profile(sender, instance, created, **kwargs):
    logs.save()