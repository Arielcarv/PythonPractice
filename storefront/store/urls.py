from django.urls import path, include
from rest_framework.routers import DefaultRouter
from store.views import ProductViewSet, CollectionViewSet

router = DefaultRouter()
router.register("products", ProductViewSet, basename="products")
router.register("collections", CollectionViewSet, basename="collections")

urlpatterns = [
    path("", include(router.urls)),
]
