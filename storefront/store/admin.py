from typing import List, Tuple, Any

from django.contrib import admin, messages
from django.db.models import QuerySet, Count
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html, urlencode

from store.models import Product, Customer, Promotion, Order, Address, Collection, OrderItem, Cart

admin.AdminSite.site_header = "Storefront Admin"
admin.AdminSite.site_title = "Storefront Admin Portal"
admin.AdminSite.index_title = "Storefront Administration"


class InventoryFilter(admin.SimpleListFilter):
    title = "inventory"
    parameter_name = "inventory"

    def lookups(self, request: HttpRequest, model_admin: admin.ModelAdmin) -> List[Tuple[Any, str]]:
        return [("0>=,<=10", "Low"), (">10", "OK")]

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet:
        if self.value() == "0>=,<=10":
            return queryset.filter(inventory__gte=0, inventory__lte=10)
        if self.value() == ">10":
            return queryset.filter(inventory__gt=10)


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
    list_display = ["first_name", "last_name", "membership", "orders"]
    list_editable = ["membership"]
    ordering = ["first_name", "last_name"]
    search_fields = ["first_name__istartswith", "last_name__istartswith"]

    @admin.display(ordering="orders_count")
    def orders(self, customer):
        url = (
            reverse("admin:store_order_changelist")
            + "?"
            + urlencode({"customer__id": str(customer.id)})
        )
        return format_html('<a href="{}">{} Orders</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(orders_count=Count("order"))


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "quantity", "unit_price"]
    list_editable = ["quantity", "unit_price"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ["clear_inventory"]
    list_display = ["title", "unit_price", "inventory_status", "inventory", "collection_title"]
    list_editable = ["unit_price"]
    list_filter = ["collection", "last_update", InventoryFilter]
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

    @admin.action(description="Clear inventory")
    def clear_inventory(self, request: HttpRequest, queryset: QuerySet):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f"{updated_count} products inventory were cleared successfully!",
            messages.ERROR,
        )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "placed_at", "payment_status", "customer"]
    list_editable = ["payment_status"]
    list_per_page = 100
    list_select_related = ["customer"]


admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(Promotion)
