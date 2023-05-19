from decimal import Decimal
from rest_framework import serializers
from store.models import Product, Cart, Collection, Review


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title", "products_count"]

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "slug",
            "inventory",
            "unit_price",
            "price_with_taxes",
            "collection",
        ]

    price_with_taxes = serializers.SerializerMethodField(method_name="calculate_tax")

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)

    """ def create(self, validated_data):
        product = Product(**validated_data)
        product.save()
        return product """

    """ def update(self, instance, validated_data):
        instance.unit_price = validated_data.get("unit_price")
        instance.save()
        return instance """


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "name", "date", "description"]

    def create(self, validated_data):
        product_id = self.context.get("product_id")
        return Review.objects.create(product_id=product_id, **validated_data)


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Cart
        fields = ["id"]
