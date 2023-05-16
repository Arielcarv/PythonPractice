from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from store.models import Collection, Product
from store.serializers import CollectionSerializer, ProductSerializer


class ProductViewSet(ModelViewSet):
    def get_queryset(self):
        return Product.objects.select_related("collection").all()

    def get_serializer_class(self):
        return ProductSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitem_set.count() > 0:
            return Response(
                {"error": "Product cannot be deleted because it's associated with an order item."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        serializer = ProductSerializer(product)
        product.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CollectionViewSet(ModelViewSet):
    def get_queryset(self):
        return Collection.objects.annotate(products_count=Count("products"))

    def get_serializer_class(self):
        return CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response(
                {"error": "Collection cannot be deleted because it includes one or more products."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        serializer = CollectionSerializer(collection)
        collection.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)
