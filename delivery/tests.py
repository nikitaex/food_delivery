from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Restaurant, Meal, CartMeal, Cart, Customer

User = get_user_model()


class AppTestCases(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username='TestUser', password='password')
        self.restaurant = Restaurant.objects.create(name='TestRestaurant',
                                                    slug='test-restaurant-slug',
                                                    address='test-address',
                                                    email='test-email',
                                                    )
        self.meal = Meal.objects.create(title='test-title',
                                        description='test-description',
                                        price=Decimal('30.00'),
                                        discount=0,
                                        restaurant=self.restaurant,
                                        slug='test-meal-slug',
                                        )
        self.customer = Customer.objects.create(user=self.user, phone='1232134', home_address='address')
        self.cart = Cart.objects.create(owner=self.customer,
                                        meals=self.meal,
                                        )
        self.cart_meal = CartMeal.objects.create(user=self.customer,
                                                 cart=self.cart,
                                                 meal=self.meal,
                                                 )

    def test_add_to_cart(self):
        self.cart.meals.add(self.cart_meal)
        self.assertIn(self.cart_meal, self.cart.meals.all())
        self.assertEqual(self.cart_meal.count(), 1)
