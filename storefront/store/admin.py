from django.contrib import admin

from store.models import Product, Customer, Promotion, Order, Address, Collection, OrderItem, Cart

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Promotion)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Collection)
admin.site.register(OrderItem)
admin.site.register(Cart)
