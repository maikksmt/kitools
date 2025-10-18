from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class StarterGuide(models.Model):
    slug = models.SlugField(unique=True, default="default")
    title = models.CharField(max_length=160, default="Starter-Guide")
    intro = models.TextField(blank=True)
    hero_title = models.CharField(max_length=160, blank=True)
    hero_subtitle = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class StarterSection(models.Model):
    guide = models.ForeignKey(StarterGuide, on_delete=models.CASCADE, related_name="sections")
    title = models.CharField(max_length=160)
    body = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.guide}: {self.title}"


CONTENT_KIND_CHOICES = [
    ("guide", "Guide"),
    ("prompt", "Prompt"),
    ("usecase", "Use-Case"),
    ("tool", "Tool"),
    ("comparison", "Vergleich"),
    ("link", "Externer Link"),
]


class StarterItem(models.Model):
    section = models.ForeignKey(StarterSection, on_delete=models.CASCADE, related_name="items")
    kind = models.CharField(max_length=20, choices=CONTENT_KIND_CHOICES, default="guide")

    # Entweder interne Verknüpfung via GenericRelation …
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")

    # … oder eine URL (für externe/noch nicht vorhandene Inhalte)
    override_url = models.URLField(blank=True)

    # Anzeige-Overrides
    title_override = models.CharField(max_length=200, blank=True)
    teaser_override = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title_override or f"{self.kind} item #{self.pk}"

    def get_title(self):
        if self.title_override:
            return self.title_override
        obj = self.content_object
        return getattr(obj, "title", None) or getattr(obj, "name", None) or "Item"

    def get_teaser(self):
        if self.teaser_override:
            return self.teaser_override
        obj = self.content_object
        return getattr(obj, "excerpt", None) or getattr(obj, "short_desc", None) or ""

    def get_url(self):
        if self.override_url:
            return self.override_url
        obj = self.content_object
        # Erwarte, dass deine Models `get_absolute_url()` haben; sonst hier per reverse() cases bauen.
        if obj and hasattr(obj, "get_absolute_url"):
            return obj.get_absolute_url()
        return "#"
