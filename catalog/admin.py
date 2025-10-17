from django.contrib import admin
from .models import Category, Tool, PricingTier, AffiliateProgram


class PricingInline(admin.TabularInline):
    model = PricingTier
    extra = 1


class AffiliateInline(admin.TabularInline):
    model = AffiliateProgram
    extra = 0


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'free_tier', 'rating', 'is_featured')
    list_filter = ('free_tier', 'is_featured', 'categories')
    search_fields = ('name', 'vendor', 'short_desc')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [PricingInline, AffiliateInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(PricingTier)
admin.site.register(AffiliateProgram)
