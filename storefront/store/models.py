from django.db import models


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey("Collection", on_delete=models.PROTECT, related_name="products")
    promotions = models.ManyToManyField(Promotion, related_name="products")

    def __str__(self):
        return self.title

    @property
    def price_display(self):
        return f"${self.price:.2f}"


class Customer(models.Model):
    MEMBERSHIP_CHOICES = [
        ("G", "Gold"),
        ("S", "Silver"),
        ("B", "Bronze"),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default="B")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ("P", "Pending"),
        ("C", "Completed"),
        ("F", "Failed"),
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default="P")
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="orders")

    def __str__(self):
        return f"Order #{self.id}"


class Address(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, primary_key=True, related_name="addresses"
    )
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)


class Collection(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    products = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, related_name="collections"
    )

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.title} x{self.quantity}"


class Cart(models.Model):
    products = models.ManyToManyField(Product, related_name="carts")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart #{self.id}"
