from rest_framework import serializers
from .models import Entrepreneur, WorkImage


class WorkImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkImage
        fields = "__all__"


class EntrepreneurSerializer(serializers.ModelSerializer):
    works = WorkImageSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Entrepreneur
        fields = "__all__"