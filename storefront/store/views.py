from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Product
from store.serializers import ProductSerializer


@api_view(["GET", "POST"])
def product_list(request):
    if request.method == "GET":
        all_products = Product.objects.select_related("collection").all()
        serializer = ProductSerializer(all_products, many=True, context={"request": request})
        return Response(serializer.data)
    serializer = ProductSerializer(data=request.data)
    return Response("OK")


@api_view()
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view()
def collection_detail(request, pk):
    return Response("OK")
