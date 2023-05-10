from decimal import Decimal
from rest_framework import serializers
from store.models import Product, Collection


class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, source="unit_price")
    price_wit_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset=Collection.objets.all()
    # )
    # collection = serializers.StringRelatedField()
    # collection = CollectionSerializer()
    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(), view_name="collection_detail"
    )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
