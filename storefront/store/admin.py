from django.contrib import admin
from django.db.models import QuerySet, Count
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html, urlencode

from store.models import Product, Customer, Promotion, Order, Address, Collection, OrderItem, Cart

admin.AdminSite.site_header = "Storefront Admin"
admin.AdminSite.site_title = "Storefront Admin Portal"
admin.AdminSite.index_title = "Storefront Administration"


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "products_count"]

    @admin.display(ordering="products_count")
    def products_count(self, collection):
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"collection__id": str(collection.id)})
        )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(products_count=Count("product"))


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership"]
    list_editable = ["membership"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "quantity", "unit_price"]
    list_editable = ["quantity", "unit_price"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "unit_price", "inventory_status", "collection_title"]
    list_editable = ["unit_price"]
    list_per_page = 100
    list_select_related = ["collection"]

    @admin.display(ordering="collection__title")
    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory > 10:
            return "OK"
        if 0 > product.inventory <= 10:
            return "Low"
        return "Out"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "placed_at", "payment_status", "customer"]
    list_editable = ["payment_status"]
    list_per_page = 100
    list_select_related = ["customer"]


admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(Promotion)
