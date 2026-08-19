import uuid

from django.shortcuts import get_object_or_404

from rest_framework import (
    status,
    viewsets,
)
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from .models import (
    Entrepreneur,
    WorkImage,
    EntrepreneurLike,
)

from .serializers import (
    EntrepreneurSerializer,
)


# =========================================================
# ENTREPRENEUR VIEWSET
# =========================================================

class EntrepreneurViewSet(
    viewsets.ModelViewSet
):

    # =====================================================
    # QUERYSET
    # =====================================================

    queryset = (
        Entrepreneur.objects
        .prefetch_related(
            "works",
            "likes",
        )
        .all()
        .order_by(
            "-created_at"
        )
    )

    serializer_class = EntrepreneurSerializer

    # =====================================================
    # DEFAULT PERMISSIONS
    # =====================================================

    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    # =====================================================
    # PERMISSIONS BY ACTION
    # =====================================================

    def get_permissions(self):

        """
        Public:

        - View entrepreneurs
        - View individual entrepreneur
        - Like
        - Unlike

        Authentication required:

        - Create
        - Update
        - Delete
        """

        if self.action == "like":

            return [
                AllowAny()
            ]

        return [
            permission()
            for permission
            in self.permission_classes
        ]

    # =====================================================
    # SERIALIZER CONTEXT
    # =====================================================

    def get_serializer_context(self):

        context = super().get_serializer_context()

        context["request"] = self.request

        return context

    # =====================================================
    # CREATE ENTREPRENEUR
    # =====================================================

    def perform_create(
        self,
        serializer,
    ):

        entrepreneur = serializer.save()

        self.save_work_images(
            entrepreneur
        )

    # =====================================================
    # UPDATE ENTREPRENEUR
    # =====================================================

    def perform_update(
        self,
        serializer,
    ):

        entrepreneur = serializer.save()

        self.save_work_images(
            entrepreneur
        )

    # =====================================================
    # SAVE WORK IMAGES
    # =====================================================

    def save_work_images(
        self,
        entrepreneur,
    ):

        work_image_fields = [
            "work_image_1",
            "work_image_2",
            "work_image_3",
        ]

        for field in work_image_fields:

            image = (
                self.request.FILES.get(
                    field
                )
            )

            if image:

                WorkImage.objects.create(
                    entrepreneur=entrepreneur,
                    image=image,
                )

    # =====================================================
    # LIKE / UNLIKE
    # =====================================================

    @action(
        detail=True,
        methods=[
            "post",
            "delete",
        ],
        url_path="like",
    )
    def like(
        self,
        request,
        pk=None,
    ):

        print(
            "================================="
        )

        print(
            "ENTREPRENEUR LIKE ENDPOINT"
        )

        print(
            "METHOD:",
            request.method,
        )

        print(
            "ENTREPRENEUR ID:",
            pk,
        )

        print(
            "DATA:",
            request.data,
        )

        print(
            "QUERY PARAMS:",
            request.query_params,
        )

        print(
            "================================="
        )

        # =================================================
        # GET ENTREPRENEUR
        # =================================================

        entrepreneur = get_object_or_404(
            Entrepreneur,
            pk=pk,
        )

        # =================================================
        # LIKE
        # =================================================

        if request.method == "POST":

            visitor_id = (
                request.data.get(
                    "visitor_id"
                )
            )

            print(
                "LIKE visitor_id:",
                visitor_id,
            )

            # ---------------------------------------------
            # Visitor ID required
            # ---------------------------------------------

            if not visitor_id:

                return Response(
                    {
                        "detail":
                        "visitor_id is required."
                    },
                    status=(
                        status.HTTP_400_BAD_REQUEST
                    ),
                )

            # ---------------------------------------------
            # Validate UUID
            # ---------------------------------------------

            try:

                visitor_id = uuid.UUID(
                    str(visitor_id)
                )

            except (
                ValueError,
                TypeError,
            ):

                return Response(
                    {
                        "detail":
                        "Invalid visitor_id."
                    },
                    status=(
                        status.HTTP_400_BAD_REQUEST
                    ),
                )

            # ---------------------------------------------
            # Create or retrieve like
            # ---------------------------------------------

            like, created = (
                EntrepreneurLike.objects
                .get_or_create(
                    entrepreneur=entrepreneur,
                    visitor_id=visitor_id,
                )
            )

            # ---------------------------------------------
            # Current count
            # ---------------------------------------------

            likes_count = (
                EntrepreneurLike.objects
                .filter(
                    entrepreneur=entrepreneur
                )
                .count()
            )

            print(
                "LIKE CREATED:",
                created,
            )

            print(
                "LIKES COUNT:",
                likes_count,
            )

            # ---------------------------------------------
            # Response
            # ---------------------------------------------

            return Response(
                {
                    "liked": True,
                    "created": created,
                    "likes_count": likes_count,
                },
                status=status.HTTP_200_OK,
            )

        # =================================================
        # UNLIKE
        # =================================================

        if request.method == "DELETE":

            visitor_id = (
                request.query_params.get(
                    "visitor_id"
                )
            )

            print(
                "UNLIKE visitor_id:",
                visitor_id,
            )

            # ---------------------------------------------
            # Visitor ID required
            # ---------------------------------------------

            if not visitor_id:

                return Response(
                    {
                        "detail":
                        "visitor_id is required."
                    },
                    status=(
                        status.HTTP_400_BAD_REQUEST
                    ),
                )

            # ---------------------------------------------
            # Validate UUID
            # ---------------------------------------------

            try:

                visitor_id = uuid.UUID(
                    str(visitor_id)
                )

            except (
                ValueError,
                TypeError,
            ):

                return Response(
                    {
                        "detail":
                        "Invalid visitor_id."
                    },
                    status=(
                        status.HTTP_400_BAD_REQUEST
                    ),
                )

            # ---------------------------------------------
            # Delete like
            # ---------------------------------------------

            deleted_count, _ = (
                EntrepreneurLike.objects
                .filter(
                    entrepreneur=entrepreneur,
                    visitor_id=visitor_id,
                )
                .delete()
            )

            # ---------------------------------------------
            # Current count
            # ---------------------------------------------

            likes_count = (
                EntrepreneurLike.objects
                .filter(
                    entrepreneur=entrepreneur
                )
                .count()
            )

            print(
                "LIKE DELETED:",
                deleted_count,
            )

            print(
                "LIKES COUNT:",
                likes_count,
            )

            # ---------------------------------------------
            # Response
            # ---------------------------------------------

            return Response(
                {
                    "liked": False,
                    "deleted": (
                        deleted_count > 0
                    ),
                    "likes_count": likes_count,
                },
                status=status.HTTP_200_OK,
            )