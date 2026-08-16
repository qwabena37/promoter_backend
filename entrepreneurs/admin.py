from django.contrib import admin

from .models import Entrepreneur, WorkImage


class WorkImageInline(admin.TabularInline):
    model = WorkImage
    extra = 3
    max_num = 3


@admin.register(Entrepreneur)
class EntrepreneurAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "title",
        "location",
        "featured",
        "created_at",
    )

    list_filter = (
        "featured",
    )

    search_fields = (
        "name",
        "title",
        "location",
        "description",
    )

    list_editable = (
        "featured",
    )

    readonly_fields = (
        "created_at",
    )

    fieldsets = (
        (
            "Entrepreneur Information",
            {
                "fields": (
                    "name",
                    "title",
                    "location",
                    "description",
                    "profile_image",
                    "featured",
                )
            },
        ),

        (
            "Video",
            {
                "fields": (
                    "video",
                )
            },
        ),

        (
            "Social Media",
            {
                "fields": (
                    "whatsapp",
                    "instagram",
                    "facebook",
                    "tiktok",
                    "youtube",
                    "website",
                )
            },
        ),

        (
            "System Information",
            {
                "fields": (
                    "created_at",
                )
            },
        ),
    )

    inlines = [
        WorkImageInline
    ]