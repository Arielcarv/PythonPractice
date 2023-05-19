from django.db import models
from django.core.validators import MinValueValidator
from uuid import uuid4


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self) -> str:
        return self.description


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        "Product", on_delete=models.SET_NULL, null=True, related_name="+"
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["title"]


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.1, message="Unit price can't be less than 0.1 .")],
    )
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name="products")
    promotions = models.ManyToManyField(Promotion, blank=True)

    def __str__(self) -> str:
        return self.title

    @property
    def price_display(self):
        return f"${self.unit_price:.2f}"

    class Meta:
        ordering = ["title"]


class Customer(models.Model):
    MEMBERSHIP_GOLD = "G"
    MEMBERSHIP_SILVER = "S"
    MEMBERSHIP_BRONZE = "B"
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_GOLD, "Gold"),
        (MEMBERSHIP_SILVER, "Silver"),
        (MEMBERSHIP_BRONZE, "Bronze"),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE
    )
    # created_at = models.DateTimeField(auto_now_add=True)
    # orders = models.ForeignKey("Order", on_delete=models.PROTECT, related_name="+")

    class Meta:
        db_table = "store_customer"
        ordering = ["first_name", "last_name"]
        indexes = [
            models.Index(fields=["first_name", "last_name"]),
        ]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    PAYMENT_STATUS_PENDING = "P"
    PAYMENT_STATUS_COMPLETE = "C"
    PAYMENT_STATUS_FAILED = "F"
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, "Pending"),
        (PAYMENT_STATUS_COMPLETE, "Completed"),
        (PAYMENT_STATUS_FAILED, "Failed"),
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING
    )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"Order #{self.id}"

    class Meta:
        ordering = ["-placed_at"]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.product.title} x{self.quantity}"

    class Meta:
        ordering = ["id"]


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Cart #{self.id}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = [["cart", "product"]]


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
