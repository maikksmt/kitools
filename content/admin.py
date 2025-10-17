from django.contrib import admin
from .models import Guide, Prompt, UseCase


@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at')
    search_fields = ('title', 'excerpt')
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at')
    search_fields = ('title', 'use_case')
    prepopulated_fields = {"slug": ("title",)}


@admin.register(UseCase)
class UseCaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'persona')
    prepopulated_fields = {"slug": ("title",)}
