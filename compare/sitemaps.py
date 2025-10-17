# compare/sitemaps.py
from django.contrib.sitemaps import Sitemap
from .models import Comparison


class ComparisonSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Comparison.objects.all()

    def lastmod(self, obj):
        return getattr(obj, "updated_at", None)

    def location(self, obj):
        return f"/vergleiche/{obj.slug}/"
