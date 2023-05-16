from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from store.views import CollectionViewSet, ProductViewSet, ReviewViewSet

router = DefaultRouter()
router.register("products", ProductViewSet, basename="products")
router.register("collections", CollectionViewSet, basename="collections")

products_router = NestedDefaultRouter(router, r"products", lookup="product")
products_router.register(r"reviews", ReviewViewSet, basename="reviews")

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(products_router.urls)),
]
