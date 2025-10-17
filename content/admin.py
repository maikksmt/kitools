# content/admin.py
from django.contrib import admin
from .models import Guide, Prompt, UseCase
from django.utils import timezone


class PublishableAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "published_at", "updated_at", "author")
    list_filter = ("status", "author", "published_at", "updated_at")
    search_fields = ("title", "slug", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
    actions = ("make_published", "make_draft")
    readonly_fields = ("published_at", "updated_at")

    @admin.action(description="Als veröffentlicht markieren")
    def make_published(self, request, queryset):
        updated = queryset.update(
            status="published", published_at=timezone.now())
        self.message_user(request, f"{updated} Einträge veröffentlicht.")

    @admin.action(description="Als Entwurf markieren")
    def make_draft(self, request, queryset):
        updated = queryset.update(status="draft")
        self.message_user(request, f"{updated} Einträge als Entwurf markiert.")


@admin.register(Guide)
class GuideAdmin(PublishableAdmin):
    filter_horizontal = ("categories", "related_tools")


@admin.register(Prompt)
class PromptAdmin(PublishableAdmin):
    filter_horizontal = ("tools",)


@admin.register(UseCase)
class UseCaseAdmin(PublishableAdmin):
    filter_horizontal = ("tools",)
