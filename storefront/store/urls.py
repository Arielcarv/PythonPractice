from django.urls import path
from store.views import ProductList, ProductDetail, CollectionList, CollectionDetail


urlpatterns = [
    path("products/", ProductList.as_view(), name="produts_list"),
    path("products/<int:pk>", ProductDetail.as_view(), name="produt_detail"),
    path("collections/", CollectionList.as_view(), name="collection_list"),
    path("collections/<int:pk>", CollectionDetail.as_view(), name="collection_detail"),
]
