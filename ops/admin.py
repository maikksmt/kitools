from django.contrib import admin
from .models import EditorialTask


@admin.register(EditorialTask)
class EditorialTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'due_date', 'assignee')
    list_filter = ('status',)
    search_fields = ('title', 'notes')
