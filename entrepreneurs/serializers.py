from rest_framework import serializers

from .models import (
    Entrepreneur,
    WorkImage,
)


# =========================================================
# WORK IMAGE SERIALIZER
# =========================================================

class WorkImageSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = WorkImage

        fields = [
            "id",
            "image",
        ]


# =========================================================
# ENTREPRENEUR SERIALIZER
# =========================================================

class EntrepreneurSerializer(
    serializers.ModelSerializer
):

    # =====================================================
    # PROFILE IMAGE
    # =====================================================

    image = serializers.SerializerMethodField()

    # =====================================================
    # WORK IMAGES
    # =====================================================

    works = WorkImageSerializer(
        many=True,
        read_only=True,
    )

    # =====================================================
    # SOCIAL MEDIA
    # =====================================================

    socials = serializers.SerializerMethodField()

    # =====================================================
    # LIKES
    # =====================================================

    likes_count = serializers.SerializerMethodField()

    # =====================================================
    # META
    # =====================================================

    class Meta:

        model = Entrepreneur

        fields = [
            "id",
            "name",
            "title",
            "location",
            "description",
            "profile_image",
            "image",
            "video",
            "works",
            "whatsapp",
            "instagram",
            "facebook",
            "tiktok",
            "youtube",
            "website",
            "linkedIn",
            "socials",
            "featured",
            "likes_count",
            "created_at",
        ]

        read_only_fields = [
            "image",
            "works",
            "socials",
            "likes_count",
            "created_at",
        ]

    # =====================================================
    # PROFILE IMAGE
    # =====================================================

    def get_image(self, obj):

        if not obj.profile_image:
            return None

        try:

            return obj.profile_image.url

        except Exception as error:

            print(
                f"Error loading profile image "
                f"for entrepreneur {obj.id}: "
                f"{error}"
            )

            return None

    # =====================================================
    # LIKES COUNT
    # =====================================================

    def get_likes_count(self, obj):

        return obj.likes.count()

    # =====================================================
    # SOCIALS
    # =====================================================

    def get_socials(self, obj):

        return {
            "whatsapp": obj.whatsapp or "",
            "instagram": obj.instagram or "",
            "facebook": obj.facebook or "",
            "tiktok": obj.tiktok or "",
            "youtube": obj.youtube or "",

            # IMPORTANT:
            # Model field is linkedIn
            "linkedin": obj.linkedIn or "",

            "website": obj.website or "",
        }