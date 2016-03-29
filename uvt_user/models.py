from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class UvtUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='uvt_user')
    first_name = models.CharField(max_length=255, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    ANR = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.full_name
