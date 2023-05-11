from django.urls import path
from store.views import product_list, product_detail, collection_list, collection_detail


urlpatterns = [
    path("products/", product_list, name="produts_list"),
    path("products/<int:id>", product_detail, name="produt_detail"),
    path("collections/", collection_list, name="collection_detail"),
    path("collections/<int:pk>", collection_detail, name="collection_detail"),
]
