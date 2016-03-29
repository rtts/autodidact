from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

from .models import UvtUser

class UvtUserInline(admin.StackedInline):
    model = UvtUser
    can_delete = False
    verbose_name_plural = 'Uvt user information'

class UserAdmin(BaseUserAdmin):
    save_on_top = True
    inlines = [UvtUserInline]
    list_display = ['username', 'uvt_first_name', 'uvt_full_name', 'uvt_ANR', 'uvt_email', 'is_staff']

    def uvt_first_name(self, user):
        if hasattr(user, 'uvt_user'):
            return user.uvt_user.first_name
        else:
            return ''

    def uvt_full_name(self, user):
        if hasattr(user, 'uvt_user'):
            return user.uvt_user.full_name
        else:
            return ''

    def uvt_ANR(self, user):
        if hasattr(user, 'uvt_user'):
            return user.uvt_user.ANR
        else:
            return ''

    def uvt_email(self, user):
        if hasattr(user, 'uvt_user'):
            return user.uvt_user.email
        else:
            return ''

# Re-register UserAdmin
admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdmin)
