from django.contrib import admin
from .models import StarterGuide, StarterSection, StarterItem


class StarterItemInline(admin.TabularInline):
    model = StarterItem
    extra = 0
    fields = ("order", "kind", "content_type", "object_id", "override_url",
              "title_override", "teaser_override", "is_published")
    ordering = ("order", "id")


class StarterSectionInline(admin.StackedInline):
    model = StarterSection
    extra = 0
    fields = ("order", "title", "body")
    show_change_link = True
    ordering = ("order", "id")


@admin.register(StarterGuide)
class StarterGuideAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_published")
    inlines = [StarterSectionInline]


@admin.register(StarterSection)
class StarterSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "guide", "order")
    ordering = ("guide", "order", "id")
    inlines = [StarterItemInline]


@admin.register(StarterItem)
class StarterItemAdmin(admin.ModelAdmin):
    list_display = ("__str__", "section", "order", "is_published")
    list_filter = ("section__guide", "kind", "is_published")
    ordering = ("section__guide", "section__order", "order", "id")
