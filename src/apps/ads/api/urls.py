from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AdViewSet, ExchangeProposalViewSet

router = DefaultRouter()
router.register("ads", AdViewSet, basename="ad")
router.register("proposals", ExchangeProposalViewSet, basename="proposal")

urlpatterns = [
    path("", include(router.urls)),
]
