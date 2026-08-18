from rest_framework import serializers

from .models import Entrepreneur, WorkImage


class WorkImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkImage
        fields = [
            "id",
            "image",
        ]


class EntrepreneurSerializer(serializers.ModelSerializer):

    gallery = serializers.SerializerMethodField()
    socials = serializers.SerializerMethodField()

    class Meta:
        model = Entrepreneur

        fields = [
            "id",
            "name",
            "title",
            "location",
            "description",
            "profile_image",
            "video",
            "gallery",
            "socials",
            "featured",
            "created_at",
        ]

        read_only_fields = [
            "gallery",
            "socials",
            "created_at",
        ]

    # =====================================================
    # GALLERY
    # =====================================================

    def get_gallery(self, obj):

        gallery = []

        for work in obj.works.all():

            if not work.image:
                continue

            try:
                # Cloudinary already returns an absolute URL
                url = work.image.url

                if url:
                    gallery.append(url)

            except Exception as error:
                print(
                    f"Error loading work image {work.id}: {error}"
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

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def to_representation(self, instance):

        data = super().to_representation(instance)

        # Cloudinary profile image
        if instance.profile_image:

            try:
                data["image"] = instance.profile_image.url

            except Exception as error:
                print(
                    f"Error loading profile image "
                    f"for entrepreneur {instance.id}: {error}"
                )

                data["image"] = None

        else:
            data["image"] = None

        return data

class EntrepreneurSerializer(serializers.ModelSerializer):

    likes_count = serializers.IntegerField(
        source="likes.count",
        read_only=True
    )

    class Meta:
        model = Entrepreneur
        fields = "__all__"