
from rest_framework import serializers

from .models import Entrepreneur, WorkImage


# =========================================================
# WORK IMAGE SERIALIZER
# =========================================================

class WorkImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkImage

        fields = [
            "id",
            "image",
        ]


# =========================================================
# ENTREPRENEUR SERIALIZER
# =========================================================

class EntrepreneurSerializer(serializers.ModelSerializer):

    # =====================================================
    # CUSTOM FIELDS
    # =====================================================

    image = serializers.SerializerMethodField()

    gallery = serializers.SerializerMethodField()

    socials = serializers.SerializerMethodField()

    likes_count = serializers.IntegerField(
        source="likes.count",
        read_only=True
    )

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
            "gallery",
            "socials",
            "featured",
            "likes_count",
            "created_at",
        ]

        read_only_fields = [
            "image",
            "gallery",
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
                f"for entrepreneur {obj.id}: {error}"
            )

            return None

    # =====================================================
    # GALLERY
    # =====================================================

    def get_gallery(self, obj):

        gallery = []

        try:

            for work in obj.works.all():

                if not work.image:
                    continue

                try:

                    url = work.image.url

                    if url:
                        gallery.append(url)

                except Exception as error:

                    print(
                        f"Error loading work image "
                        f"{work.id}: {error}"
                    )

        except Exception as error:

            print(
                f"Error loading gallery for "
                f"entrepreneur {obj.id}: {error}"
            )

        return gallery

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
            "website": obj.website or "",
        }
