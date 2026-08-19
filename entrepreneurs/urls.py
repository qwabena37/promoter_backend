from rest_framework.routers import DefaultRouter

from .views import EntrepreneurViewSet


router = DefaultRouter()

router.register(
    r"entrepreneurs",
    EntrepreneurViewSet,
    basename="entrepreneur",
)

urlpatterns = router.urls