# catalog/sitemaps.py
from django.contrib.sitemaps import Sitemap
from .models import Tool


class ToolSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Tool.objects.all()

    def lastmod(self, obj):
        return getattr(obj, "updated_at", None)

    def location(self, obj):
        return f"/catalog/{obj.slug}/" if hasattr(obj, "slug") else "/"
