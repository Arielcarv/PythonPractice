from django.contrib import admin

from store.models import Product, Customer, Promotion, Order, Address, Collection, OrderItem, Cart

admin.AdminSite.site_header = "Storefront Admin"
admin.AdminSite.site_title = "Storefront Admin Portal"
admin.AdminSite.index_title = "Storefront Administration"


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
    list_display = ["title", "unit_price", "inventory_status"]
    list_editable = ["unit_price"]
    list_per_page = 100

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory > 10:
            return "OK"
        if 0 <= product.inventory <= 10:
            return "Low"
        return "Out"


admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(Collection)
admin.site.register(Order)
admin.site.register(Promotion)
