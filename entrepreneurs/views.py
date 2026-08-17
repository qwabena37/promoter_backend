from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Entrepreneur
from .serializers import EntrepreneurSerializer


class EntrepreneurViewSet(viewsets.ModelViewSet):
    queryset = Entrepreneur.objects.all().order_by("-created_at")
    serializer_class = EntrepreneurSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    