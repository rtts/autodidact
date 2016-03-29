from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

from .models import UvtUser
from .utils import search_ldap, LDAPError

@receiver(post_save, sender=get_user_model())
def auto_populate_uvt_user(sender, instance, **kwargs):
    '''Auto-populates the uvt_user attribute when a regular Django user is saved'''

    user = instance
    if not hasattr(user, 'uvt_user'):
        UvtUser(user=user).save()

    # Permission has been granted by TiU's legal department for
    # retrieving the following data:
    try:
        (
            user.uvt_user.first_name,
            user.uvt_user.full_name,
            user.uvt_user.ANR,
            user.uvt_user.email
        ) = search_ldap(user.username)
        user.uvt_user.save()
    except LDAPError:
        pass
