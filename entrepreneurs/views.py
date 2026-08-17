from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Entrepreneur, WorkImage
from .serializers import EntrepreneurSerializer


class EntrepreneurViewSet(viewsets.ModelViewSet):

    queryset = Entrepreneur.objects.all().order_by("-created_at")

    serializer_class = EntrepreneurSerializer

    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]

    # =====================================================
    # CREATE ENTREPRENEUR
    # =====================================================

    def perform_create(self, serializer):

        # ---------------------------------------------
        # Save entrepreneur first
        # ---------------------------------------------

        entrepreneur = serializer.save()

        # ---------------------------------------------
        # Save work images
        # ---------------------------------------------

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

    # =====================================================
    # UPDATE ENTREPRENEUR
    # =====================================================

    def perform_update(self, serializer):

        # ---------------------------------------------
        # Update entrepreneur
        # ---------------------------------------------

        entrepreneur = serializer.save()

        # ---------------------------------------------
        # Save newly uploaded work images
        #
        # Existing images are NOT deleted.
        # ---------------------------------------------

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