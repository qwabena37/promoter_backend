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

    def get_gallery(self, obj):

        request = self.context.get("request")

        images = obj.works.all()

        gallery = []

        for image in images:

            if not image.image:
                continue

            url = image.image.url

            if request:
                url = request.build_absolute_uri(url)

            gallery.append(url)

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

        request = self.context.get("request")

        if instance.profile_image:

            url = instance.profile_image.url

            if request:
                url = request.build_absolute_uri(url)

            data["image"] = url

        else:

            data["image"] = None

        return data