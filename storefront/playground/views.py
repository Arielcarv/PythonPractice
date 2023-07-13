from django.core.cache import cache
from django.core.mail import BadHeaderError, EmailMessage
from django.db.models import Value, F, Func, Min, Count, ExpressionWrapper, DecimalField
from django.db.models.functions import Concat
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from playground.tasks import notify_customers
from rest_framework.views import APIView
from store.models import Product, OrderItem, Order, Customer
from tags.models import TaggedItem
from templated_mail.mail import BaseEmailMessage
import requests


def home(request: HttpRequest) -> HttpResponse:
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

    """Database Functions"""
    database_function_queryset = Customer.objects.annotate(
        full_name_1=Func(
            F("user__first_name"), Value(" "), F("user__last_name"), function="CONCAT"
        ),
        full_name_2=Concat("user__first_name", Value(" "), "user__last_name"),
    )

    """Orders by Customer"""
    orders_by_customer = Customer.objects.annotate(oders_count=Count("order"))

    """Expressions Wrappers"""
    discounted_price = Product.objects.annotate(
        discounted_price=ExpressionWrapper(F("unit_price") * 0.8, output_field=DecimalField())
    )

    """Content Types"""
    tagged_items = TaggedItem.objects.get_tags_for(Product, 1)

    context = {
        "products": list(products),
        "last_5_orders": last_5_orders,
        "aggregation_result": aggregation_result,
        "annotate_queryset": list(annotate_queryset),
        "database_function_queryset": list(database_function_queryset),
        "orders_by_customer": list(orders_by_customer),
        "discounted_price": list(discounted_price),
        "tagged_items": list(tagged_items),
    }
    return render(request, "home.html", context)


def say(request: HttpRequest) -> HttpResponse:
    try:
        # send_mail("subject", "message", "info@ariel.com", ["bob@ariel.com"])
        # mail_admins("subject", "message", html_message="message")
        message = EmailMessage("subject", "message", "info@ariel.com", ["bob@ariel.com"])
        message.attach_file("playground/static/images/one-piece-jolly-roger.png")
        message.send()
    except BadHeaderError:
        pass
    return render(request, "hello.html")


def email_sender(request: HttpRequest) -> HttpResponse:
    try:
        message = BaseEmailMessage(
            template_name="emails/hello.html",
            context={"name": "Ariel"},
        )
        message.send(["bob@ariel.com"])
    except BadHeaderError:
        pass
    return render(request, "hello.html")


def celery_email_sender(request: HttpRequest) -> HttpResponse:
    notify_customers.delay("Hello")
    return render(request, "hello.html")


def simulate_delay(request: HttpRequest) -> HttpResponse:
    requests.get("https://httpbin.org/delay/2")
    return render(request, "hello.html", {"name": "Ariel"})


def simulate_delay_caching(request: HttpRequest) -> HttpResponse:
    cache_key = "httpbin_result"
    if cache.get(cache_key) is None:
        response = requests.get("https://httpbin.org/delay/2")
        data = response.json()
        cache.set(cache_key, data)
    return render(request, "hello.html", {"name": cache.get(cache_key)})


@cache_page(5 * 60)
def simulate_delay_caching_with_decorator(request: HttpRequest) -> HttpResponse:
    response = requests.get("https://httpbin.org/delay/2")
    data = response.json()
    return render(request, "hello.html", {"name": data})


class CachingView(APIView):
    @method_decorator(cache_page(5 * 60))
    def get(self, request):
        response = requests.get("https://httpbin.org/delay/2")
        data = response.json()
        return render(request, "hello.html", {"name": data})
