
import uuid

from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from rest_framework.response import Response

from .models import (
    Entrepreneur,
    WorkImage,
    EntrepreneurLike,
)
from .serializers import EntrepreneurSerializer


class EntrepreneurViewSet(viewsets.ModelViewSet):

    queryset = (
        Entrepreneur.objects
        .prefetch_related("works")
        .all()
        .order_by("-created_at")
    )

    serializer_class = EntrepreneurSerializer

    # =====================================================
    # PERMISSIONS
    # =====================================================

    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]

    def get_permissions(self):
        """
        Allow anyone to view, like and unlike entrepreneurs.

        Creating, updating and deleting entrepreneurs still
        requires authentication.
        """

        if self.action in ["like", "unlike"]:
            return [AllowAny()]

        return [permission() for permission in self.permission_classes]

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

    def perform_create(self, serializer):

        entrepreneur = serializer.save()

        self.save_work_images(entrepreneur)

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

    # ===================================================== # LIKE / UNLIKE ENTREPRENEUR # ===================================================== @action( detail=True, methods=["post", "delete"], url_path="like", ) def like(self, request, pk=None): entrepreneur = get_object_or_404( Entrepreneur, pk=pk ) # ------------------------------------------------- # LIKE # ------------------------------------------------- if request.method == "POST": visitor_id = request.data.get( "visitor_id" ) if not visitor_id: return Response( { "detail": "visitor_id is required." }, status=status.HTTP_400_BAD_REQUEST ) # --------------------------------------------- # Validate UUID # --------------------------------------------- try: visitor_id = uuid.UUID( str(visitor_id) ) except (ValueError, TypeError): return Response( { "detail": "Invalid visitor_id." }, status=status.HTTP_400_BAD_REQUEST ) # --------------------------------------------- # Create like if it doesn't already exist # --------------------------------------------- like, created = ( EntrepreneurLike.objects.get_or_create( entrepreneur=entrepreneur, visitor_id=visitor_id, ) ) # --------------------------------------------- # Return current state # --------------------------------------------- return Response( { "liked": True, "created": created, "likes_count": entrepreneur.likes.count(), }, status=status.HTTP_200_OK ) # ================================================= # UNLIKE # ================================================= if request.method == "DELETE": visitor_id = request.query_params.get( "visitor_id" ) if not visitor_id: return Response( { "detail": "visitor_id is required." }, status=status.HTTP_400_BAD_REQUEST ) # --------------------------------------------- # Validate UUID # --------------------------------------------- try: visitor_id = uuid.UUID( str(visitor_id) ) except (ValueError, TypeError): return Response( { "detail": "Invalid visitor_id." }, status=status.HTTP_400_BAD_REQUEST ) # --------------------------------------------- # Find and remove like # --------------------------------------------- deleted_count, _ = ( EntrepreneurLike.objects.filter( entrepreneur=entrepreneur, visitor_id=visitor_id, ).delete() ) # --------------------------------------------- # Return updated state # --------------------------------------------- return Response( { "liked": False, "deleted": deleted_count > 0, "likes_count": entrepreneur.likes.count(), }, status=status.HTTP_200_OK )

