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

            # Social fields (must be included to save them)
            "whatsapp",
            "instagram",
            "facebook",
            "tiktok",
            "youtube",
            "website",

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

    def get_gallery(self, obj):
        gallery = []

        for image in obj.works.all():

            if not image.image:
                continue

            try:
                gallery.append(image.image.url)
            except Exception:
                continue

        return gallery

    def get_socials(self, obj):
        return {
            "whatsapp": obj.whatsapp,
            "instagram": obj.instagram,
            "facebook": obj.facebook,
            "tiktok": obj.tiktok,
            "youtube": obj.youtube,
            "website": obj.website,
        }

    def to_representation(self, instance):

        data = super().to_representation(instance)

        try:
            data["image"] = (
                instance.profile_image.url
                if instance.profile_image
                else None
            )
        except Exception:
            data["image"] = None

        return data