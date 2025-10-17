# content/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Guide, Prompt, UseCase


class _BasePublishableSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def lastmod(self, obj):
        return getattr(obj, "updated_at", None) or getattr(obj, "published_at", None)


class GuideSitemap(_BasePublishableSitemap):
    def items(self):
        return Guide.published.all()

    def location(self, obj):
        return f"/guides/{obj.slug}/"


class PromptSitemap(_BasePublishableSitemap):
    def items(self):
        return Prompt.published.all()

    def location(self, obj):
        return f"/prompts/{obj.slug}/"


class UseCaseSitemap(_BasePublishableSitemap):
    def items(self):
        return UseCase.published.all()

    def location(self, obj):
        return f"/use-cases/{obj.slug}/"
