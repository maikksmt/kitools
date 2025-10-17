from django.db import models
from catalog.models import Tool


class Comparison(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    intro = models.TextField(blank=True)
    tools = models.ManyToManyField(Tool, related_name='comparisons', blank=True)
    score_breakdown = models.JSONField(default=dict, blank=True)  # {tool_slug: {kriterium: score}}
    winner = models.ForeignKey(Tool, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')


class Meta:
    verbose_name = 'Vergleich'
    verbose_name_plural = 'Vergleiche'


def __str__(self):
    return self.title
