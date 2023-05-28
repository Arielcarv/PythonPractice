from decimal import Decimal
from rest_framework import serializers
from store.models import Product, Cart, CartItem, Customer, Collection, Review


class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Collection
        fields = ["id", "title", "products_count"]


class ProductSerializer(serializers.ModelSerializer):
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


class ReviewSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        product_id = self.context.get("product_id")
        return Review.objects.create(product_id=product_id, **validated_data)

    class Meta:
        model = Review
        fields = ["id", "name", "date", "description"]


class CartItemProductSerializer(serializers.ModelSerializer):
    price_with_taxes = serializers.SerializerMethodField(method_name="calculate_tax")

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)

    class Meta:
        model = Product
        fields = ["id", "title", "unit_price", "price_with_taxes"]


class CartItemSerializer(serializers.ModelSerializer):
    product = CartItemProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(read_only=True, many=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart: CartItem):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ["id", "items", "total_price"]


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, pk):
        if not Product.objects.filter(pk=pk).exists():
            raise serializers.ValidationError("There is no product with the specified ID.")
        return pk

    def save(self):
        cart_id = self.context.get("cart_id")
        product_id = self.validated_data.get("product_id")
        quantity = self.validated_data.get("quantity")
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ["id", "product_id", "quantity"]


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Customer
        fields = ["id", "user_id", "phone", "birth_date", "membership"]
