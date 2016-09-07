from django.apps import apps
from django.dispatch import receiver
from django.db.models.signals import post_migrate

@receiver(post_migrate, sender=apps.get_app_config('autodidact'))
def create_homepage(sender, **kwargs):
    '''Receiver function that populates the database with a homepage in case it doesn't exist'''

    from .models import Page
    if not Page.objects.exists():
        Page(content='***Hello, world!***').save()
