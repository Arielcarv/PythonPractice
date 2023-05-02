from django.contrib import admin

from store.models import Product, Customer, Promotion, Order, Address, Collection, OrderItem, Cart

admin.AdminSite.site_header = "Storefront Admin"
admin.AdminSite.site_title = "Storefront Admin Portal"
admin.AdminSite.index_title = "Storefront Administration"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "unit_price"]
    list_editable = ["unit_price"]
    list_per_page = 100


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership"]
    list_editable = ["membership"]


admin.site.register(Promotion)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Collection)
admin.site.register(OrderItem)
admin.site.register(Cart)
