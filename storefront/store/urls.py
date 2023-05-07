from django.urls import path
from store.views import product_list, product_detail


urlpatterns = [
    path("products/", product_list, name="produts_list"),
    path("products/<int:id>", product_detail, name="produt_detail"),
]
