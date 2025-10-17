from django.db import models
from catalog.models import Tool, Category
from taggit.managers import TaggableManager


class Guide(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    excerpt = models.CharField(max_length=240, blank=True)
    body = models.TextField()
    reading_time = models.PositiveIntegerField(default=5)
    hero_image = models.ImageField(upload_to='guides/', blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True)
    related_tools = models.ManyToManyField(Tool, blank=True)
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class Prompt(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    body = models.TextField()
    use_case = models.CharField(max_length=160, blank=True)
    examples = models.JSONField(default=list, blank=True)
    tools = models.ManyToManyField(Tool, blank=True)
    tags = TaggableManager(blank=True)
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UseCase(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    persona = models.CharField(max_length=120)
    problem = models.TextField()
    workflow_steps = models.JSONField(default=list, blank=True)
    tools = models.ManyToManyField(Tool, blank=True)
    kpi_impact = models.JSONField(default=dict, blank=True)  # {"zeitersparnis_min": 20, ...}

    def __str__(self):
        return self.title
