from rest_framework import request, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import uuid
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import action
from .models import Entrepreneur, WorkImage, EntrepreneurLike
from .serializers import EntrepreneurSerializer


class EntrepreneurViewSet(viewsets.ModelViewSet):

    queryset = (
        Entrepreneur.objects
        .prefetch_related("works")
        .all()
        .order_by("-created_at")
    )

    serializer_class = EntrepreneurSerializer

    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]

    # =====================================================
    # CREATE ENTREPRENEUR
    # =====================================================

    def perform_create(self, serializer):

        entrepreneur = serializer.save()

        self.save_work_images(entrepreneur)


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
    # =====================================================
    # UPDATE ENTREPRENEUR
    # =====================================================

    def perform_update(self, serializer):

        entrepreneur = serializer.save()

        self.save_work_images(entrepreneur)

    # =====================================================
    # SAVE WORK IMAGES
    # =====================================================

    def save_work_images(self, entrepreneur):

        work_image_fields = [
            "work_image_1",
            "work_image_2",
            "work_image_3",
        ]

        for field in work_image_fields:

            image = self.request.FILES.get(field)

            if image:

                WorkImage.objects.create(
                    entrepreneur=entrepreneur,
                    image=image
                )

    @action(
        detail=True,
        methods=["post"],
        url_path="like"
    )
    def like(self, request, pk=None):

        entrepreneur = get_object_or_404(
        Entrepreneur,
        pk=pk
        )

        visitor_id = request.data.get("visitor_id")

        if not visitor_id:
            return Response(
            {
                "detail": "visitor_id is required."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

        try:
            visitor_id = uuid.UUID(
            str(visitor_id)
            )
        except ValueError:
            return Response(
            {
                "detail": "Invalid visitor_id."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

        like, created = EntrepreneurLike.objects.get_or_create(
            entrepreneur=entrepreneur,
            visitor_id=visitor_id,
        )

        return Response(
        {
            "liked": True,
            "likes_count": entrepreneur.likes.count(),
        }
    )


@action(
    detail=True,
    methods=["delete"],
    url_path="like"
)
def unlike(self, request, pk=None):

    entrepreneur = get_object_or_404(
        Entrepreneur,
        pk=pk
    )

    visitor_id = request.query_params.get(
        "visitor_id"
    )

    if not visitor_id:
        return Response(
            {
                "detail": "visitor_id is required."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        visitor_id = uuid.UUID(
            str(visitor_id)
        )
    except ValueError:
        return Response(
            {
                "detail": "Invalid visitor_id."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    EntrepreneurLike.objects.filter(
        entrepreneur=entrepreneur,
        visitor_id=visitor_id,
    ).delete()

    return Response(
        {
            "liked": False,
            "likes_count": entrepreneur.likes.count(),
        }
    )