# content/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from catalog.models import Tool, Category
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="published")


class Publishable(models.Model):
    STATUS_CHOICES = (
        ("draft", "Entwurf"),
        ("published", "Veröffentlicht"),
    )
    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default="draft")
    published_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="%(class)s_items"
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        abstract = True

    def publish(self):
        self.status = "published"
        if not self.published_at:
            self.published_at = timezone.now()

    def save(self, *args, **kwargs):
        # Auto-Set published_at, wenn Status auf published wechselt
        if self.status == "published" and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)


class Guide(Publishable):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    excerpt = models.CharField(max_length=240, blank=True)
    body = models.TextField()
    reading_time = models.PositiveIntegerField(default=5)
    hero_image = models.ImageField(upload_to='guides/', blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True)
    related_tools = models.ManyToManyField(Tool, blank=True)

    def __str__(self):
        return self.title


class Prompt(Publishable):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    body = models.TextField()
    use_case = models.CharField(max_length=160, blank=True)
    examples = models.JSONField(default=list, blank=True)
    tools = models.ManyToManyField(Tool, blank=True)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title


class UseCase(Publishable):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    persona = models.CharField(max_length=120)
    problem = models.TextField()
    workflow_steps = models.JSONField(default=list, blank=True)
    tools = models.ManyToManyField(Tool, blank=True)
    kpi_impact = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.title
