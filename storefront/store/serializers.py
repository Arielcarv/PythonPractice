from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from store.models import Order, OrderItem, Product, Cart, CartItem, Customer, Collection, Review
from store.signals import order_created


class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Collection
        fields = ["id", "title", "products_count"]


class ProductSerializer(serializers.ModelSerializer):
    price_with_taxes = serializers.SerializerMethodField(method_name="calculate_tax")

    def calculate_tax(self, product: Product) -> Decimal:
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
    def create(self, validated_data) -> Review:
        product_id = self.context.get("product_id")
        return Review.objects.create(product_id=product_id, **validated_data)

    class Meta:
        model = Review
        fields = ["id", "name", "date", "description"]


class SimpleProductSerializer(serializers.ModelSerializer):
    price_with_taxes = serializers.SerializerMethodField(method_name="calculate_tax")

    def calculate_tax(self, product: Product) -> Decimal:
        return product.unit_price * Decimal(1.1)

    class Meta:
        model = Product
        fields = ["id", "title", "unit_price", "price_with_taxes"]


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem) -> Decimal:
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(read_only=True, many=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart: CartItem) -> Decimal:
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ["id", "items", "total_price"]


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, pk: int) -> int:
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
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ["id", "user_id", "phone", "birth_date", "membership"]


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "unit_price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "customer", "items", "placed_at", "payment_status"]


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["payment_status"]


@transaction.atomic
class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id: int) -> int:
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError("No cart with the given ID was found.")
        if CartItem.objects.fildeer(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError("The cart is empty.")
        return cart_id

    def save(self, **kwargs):
        cart_id = self.validated_data["cart_id"]
        customer = Customer.objects.get(user_id=self.context["user_id"])
        order = Order.objects.create(customer=customer)
        cart_items = CartItem.objects.select_related("product").filter(cart_id=cart_id)
        order_items = [
            OrderItem(
                order=order,
                product=item.product,
                unit_price=item.product.unit_price,
                quantity=item.quantity,
            )
            for item in cart_items
        ]

        OrderItem.objects.bulk_create(order_items)
        Cart.objects.filter(pk=cart_id).delete()

        order_created.send_robust(sender=self.__class__, order=order)

        return order
