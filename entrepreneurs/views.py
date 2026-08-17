from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Entrepreneur, WorkImage
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