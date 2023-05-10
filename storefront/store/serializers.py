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

    """ # PrimaryKeys
    collection = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objets.all()
    ) """

    """ # String Relationship
    collection = serializers.StringRelatedField() """

    """ # Nested Objects Relationship
    collection = CollectionSerializer() """

    # Hyperlink Relationship
    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(), view_name="collection_detail"
    )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
