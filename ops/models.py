from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class EditorialTask(models.Model):
    STATUS = [("open", "Offen"), ("doing", "In Arbeit"), ("done", "Erledigt")]
    title = models.CharField(max_length=180)
    type = models.CharField(max_length=120)
    status = models.CharField(max_length=20, choices=STATUS, default='open')
    due_date = models.DateField(null=True, blank=True)
    assignee = models.CharField(max_length=120, blank=True)
    notes = models.TextField(blank=True)

    # Bezug auf beliebiges Objekt
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    related = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.title
