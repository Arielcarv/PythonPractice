from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from store.views import (
    CartViewSet,
    CartItemViewSet,
    CollectionViewSet,
    CustomerViewSet,
    OrderViewSet,
    ProductViewSet,
    ProductImageViewSet,
    ReviewViewSet,
)

router = DefaultRouter()
router.register("products", ProductViewSet, basename="products")
router.register("collections", CollectionViewSet, basename="collections")
router.register("carts", CartViewSet)
router.register("customers", CustomerViewSet, basename="customers")
router.register("orders", OrderViewSet, basename="orders")
router.register("images", ProductImageViewSet, basename="images")

products_router = NestedDefaultRouter(router, r"products", lookup="product")
products_router.register(r"reviews", ReviewViewSet, basename="product-reviews")
products_router.register(r"images", ProductImageViewSet, basename="product-images")

carts_router = NestedDefaultRouter(router, r"carts", lookup="carts")
carts_router.register(r"items", CartItemViewSet, basename="cart-items")

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(products_router.urls)),
    path(r"", include(carts_router.urls)),
]
