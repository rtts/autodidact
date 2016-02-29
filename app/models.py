from django.db import models
from adminsortable.models import SortableMixin
from adminsortable.fields import SortableForeignKey

class MainModel(SortableMixin):
    order = models.PositiveIntegerField(default=0, editable=False)
    class Meta:
        ordering = ['order']

class InlineModel(SortableMixin):
    txt = models.TextField()
    main = SortableForeignKey(MainModel)
    order = models.PositiveIntegerField(default=0, editable=False)
    class Meta:
        ordering = ['order']
