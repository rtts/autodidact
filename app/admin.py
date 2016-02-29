from django.contrib import admin
from .models import *
from adminsortable.admin import SortableAdmin, NonSortableParentAdmin, SortableTabularInline

class InlineStepAdmin(SortableTabularInline):
    model = InlineModel

@admin.register(MainModel)
class MainModelAdmin(SortableAdmin):
    inlines = [InlineStepAdmin]
