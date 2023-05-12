from django.urls import path
from store.views import ProductList, ProductDetail, collection_list, collection_detail


urlpatterns = [
    path("products/", ProductList.as_view(), name="produts_list"),
    path("products/<int:id>", ProductDetail.as_view(), name="produt_detail"),
    path("collections/", collection_list, name="collection_detail"),
    path("collections/<int:pk>", collection_detail, name="collection_detail"),
]
