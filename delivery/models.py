import json
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum, F, DecimalField, IntegerField

from delivery.models_service import calculate_discount


class User(AbstractUser):
    is_restaurateur = models.BooleanField(default=False)
    is_courier = models.BooleanField(default=False)


class Restaurant(models.Model):
    """Restaurant"""

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    address = models.CharField(max_length=1024)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    meals = models.ManyToManyField('Meal', related_name='related_restaurant', blank=True)
    email = models.EmailField()

    def __str__(self):
        return self.name

    @property
    def meals(self):
        return json.dumps(Meal.objects.filter(restaurant=self).values())

    class Meta:
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'


class Meal(models.Model):
    """Meal"""

    title = models.CharField(max_length=255)
    description = models.TextField(default='The description will be later')
    price = models.DecimalField(max_digits=9, decimal_places=2)
    discount = models.IntegerField(default=0)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Meal'
        verbose_name_plural = 'Meals'


class CartMeal(models.Model):
    """Cart Meal"""

    user = models.ForeignKey('Customer', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Cart', on_delete=models.CASCADE, related_name='related_meals')
    meal = models.ForeignKey(Meal, verbose_name='Meal', on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return f"Meal {self.meal.title} from cart {self.user}"

    def save(self, *args, **kwargs):
        final_price = calculate_discount(self.meal.discount, self.qty, self.meal.price)
        self.final_price = final_price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Cart meal'
        verbose_name_plural = 'Cart meals'


class Cart(models.Model):
    """Cart"""

    owner = models.OneToOneField('Customer', on_delete=models.CASCADE)
    meals = models.ManyToManyField(CartMeal, related_name='related_cart', blank=True)
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    in_orders = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.owner} user cart"

    def save(self, *args, **kwargs):
        if self.id:
            self.total_products = self.meals.count()
            self.final_price = Cart.objects.aggregate(final_price=Sum(
                F('meals__final_price'),
                output_field=DecimalField())
            )['final_price']
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class Customer(models.Model):
    """Customer"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer')
    phone = models.CharField(max_length=20, blank=True)
    home_address = models.CharField(max_length=1024, blank=True, null=True)
    orders = models.ManyToManyField('Order', related_name='related_order', blank=True)

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class Order(models.Model):
    """User's order"""

    STATUS_NEW = 'new'
    STATUS_ACCEPTED = 'accepted for cooking'
    STATUS_COOKED = 'cooked'
    STATUS_ACCEPTED_BY_COURIER = 'handed over to the courier'
    STATUS_DELIVERED = 'delivered'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Waiting for'),
        (STATUS_ACCEPTED, 'Accepted for cooking'),
        (STATUS_COOKED, 'Cooked'),
        (STATUS_ACCEPTED_BY_COURIER, 'Accepted by the courier'),
        (STATUS_DELIVERED, 'Delivered'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='related_orders')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    cart_meal = models.ManyToManyField(CartMeal, blank=True)
    restaurant_address = models.CharField(max_length=1024)
    address = models.CharField(max_length=1024)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField(auto_now=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    courier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Order {self.customer}'s user to {self.address}"

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class Complaint(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    courier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    description = models.TextField(default=f'Complaint on courier {str(courier)}')

    def __str__(self):
        return f"The complaint of the user {str(self.customer)} about the courier {str(self.courier)}"
