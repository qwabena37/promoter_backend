from rest_framework.routers import DefaultRouter
from .views import EntrepreneurViewSet

router = DefaultRouter()
router.register(
    "entrepreneurs",
    EntrepreneurViewSet
)

urlpatterns = router.urls