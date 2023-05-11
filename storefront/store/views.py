from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Collection, Product
from store.serializers import CollectionSerializer, ProductSerializer


@api_view(["GET", "POST"])
def product_list(request):
    if request.method == "GET":
        all_products = Product.objects.select_related("collection").all()
        serializer = ProductSerializer(all_products, many=True, context={"request": request})
        return Response(serializer.data)
    serializer = ProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    if request.method == "DELETE":
        if product.orderitem_set.count() > 0:
            return Response(
                {"error": "Product cannot be deleted because it's associated with an order item."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        serializer = ProductSerializer(product)
        product.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def collection_list(request):
    if request.method == "GET":
        all_collections = Collection.objects.annotate(products_count=Count("products"))
        serializer = CollectionSerializer(all_collections, many=True)
        return Response(serializer.data)
    serializer = CollectionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def collection_detail(request, pk):
    collection = get_object_or_404(
        Collection.objects.annotate(products_count=Count("products")), pk=pk
    )

    if request.method == "GET":
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    if request.method == "DELETE":
        if collection.products.count() > 0:
            return Response(
                {"error": "Collection cannot be deleted because it includes one or more products."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        serializer = CollectionSerializer(collection)
        collection.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)
