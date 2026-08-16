from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Entrepreneur
from .serializers import EntrepreneurSerializer


class EntrepreneurViewSet(viewsets.ModelViewSet):
    queryset = Entrepreneur.objects.all().order_by("-created_at")
    serializer_class = EntrepreneurSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]