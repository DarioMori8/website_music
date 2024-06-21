from django.core.signals import request_started
from django.db.models.signals import post_migrate
from django.contrib.sessions.models import Session
from django.dispatch import receiver

@receiver(post_migrate)
def clear_sessions(sender, **kwargs):
    Session.objects.all().delete()

