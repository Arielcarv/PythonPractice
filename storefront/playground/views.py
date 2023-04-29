from django.db.models import Value, F
from django.db.models.aggregates import Count, Min
from django.shortcuts import render

from store.models import Product, OrderItem, Order, Customer


def home(request):
    """Select products that have been ordered and sort those products by title"""
    distinct_order_items = OrderItem.objects.values("product_id").distinct()
    products = Product.objects.filter(id__in=distinct_order_items).order_by("title")

    """Get the last 5 orders with their customer and items (this includes product)"""
    last_5_orders = (
        Order.objects.select_related("customer")
        .prefetch_related("orderitem_set__product")
        .order_by("-placed_at")[:5]
    )

    """Aggregation"""
    aggregation_result = Product.objects.filter(collection__id=3).aggregate(
        count=Count("id"), min_price=Min("unit_price")
    )

    """Annotate"""
    annotate_queryset = Customer.objects.annotate(
        is_new=Value(True), new_id=F("id"), new_id_plus_1=F("id") + 1
    )

    context = {
        "products": list(products),
        "last_5_orders": last_5_orders,
        "aggregation_result": aggregation_result,
        "annotate_queryset": list(annotate_queryset),
    }
    return render(request, "home.html", context)


def say(request):
    return render(request, "hello.html")
