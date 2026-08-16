from django.contrib import admin
from .models import Entrepreneur, WorkImage


class WorkImageInline(admin.TabularInline):
    model = WorkImage
    extra = 3


@admin.register(Entrepreneur)
class EntrepreneurAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "title",
        "featured",
        "created_at"
    )

    list_filter = (
        "featured",
    )

    search_fields = (
        "name",
        "title"
    )

    inlines = [
        WorkImageInline
    ]