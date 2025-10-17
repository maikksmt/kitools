from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager


class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Kategorie'
        verbose_name_plural = 'Kategorien'

    def __str__(self):
        return self.name


class Tool(models.Model):
    name = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    vendor = models.CharField(max_length=160, blank=True)
    short_desc = models.CharField(max_length=240, blank=True)
    long_desc = models.TextField(blank=True)
    website_url = models.URLField(blank=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    language_support = models.JSONField(default=list)  # z.B. ["de","en"]
    pricing_model = models.CharField(max_length=80, blank=True)  # free, freemium, subscription
    free_tier = models.BooleanField(default=False)
    monthly_price_min = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    published_at = models.DateTimeField(default=timezone.now)

    categories = models.ManyToManyField(Category, related_name='tools', blank=True)
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ['-is_featured', 'name']

    def __str__(self):
        return self.name


class PricingTier(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='pricing')
    name = models.CharField(max_length=120)
    price_month = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    price_year = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    features = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.tool.name} – {self.name}"


class AffiliateProgram(models.Model):
    COMMISSION_CHOICES = [
        ("flat", "Pauschal"),
        ("percent", "% vom Umsatz"),
        ("recurring", "Wiederkehrend"),
    ]
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='affiliates')
    network = models.CharField(max_length=120, blank=True)  # z.B. Impact, CJ, Direkt
    program_url = models.URLField(blank=True)
    commission_type = models.CharField(max_length=20, choices=COMMISSION_CHOICES, default='percent')
    commission_value = models.CharField(max_length=60, blank=True)  # z.B. "30%" oder "€50"
    cookie_days = models.IntegerField(default=30)
    tracking_note = models.CharField(max_length=240, blank=True)

    def __str__(self):
        return f"Affiliate: {self.tool.name}"
