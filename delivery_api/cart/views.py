from rest_framework.decorators import action
from rest_framework import response, status, viewsets
from django.shortcuts import get_object_or_404
import itertools

from delivery.tasks import send_order_to_restaurant
from ..cart.serializers import CartSerializer
from delivery.models import Cart, Meal, CartMeal, Customer, Order


class CartViewSet(viewsets.ModelViewSet):

    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    """To get the current user's shopping cart, go to /current_customer_cart"""

    @staticmethod
    def get_cart(user):
        if user.is_authenticated:
            return Cart.objects.get(owner=user.customer, for_anonymous_user=False)
        return Cart.objects.get(for_anonymous_user=True)

    @staticmethod
    def _get_or_create_cart_meal(customer: Customer, cart: Cart, meal: Meal):
        cart_meal, created = CartMeal.objects.get_or_create(
            user=customer,
            meal=meal,
            cart=cart,
        )
        return cart_meal, created

    @action(methods=['GET'], detail=False)
    def current_customer_cart(self, *args, **kwargs):
        cart = self.get_cart(self.request.user)
        cart_serializer = CartSerializer(cart)
        return response.Response(cart_serializer.data)

    @action(methods=['PUT'], detail=False, url_path=r'current_customer_cart/add_to_cart/(?P<meal_id>\d+)')
    def meal_add_to_cart(self, *args, **kwargs):
        cart = self.get_cart(self.request.user)
        meal = get_object_or_404(Meal, id=kwargs['meal_id'])
        cart_meal, created = self._get_or_create_cart_meal(self.request.user.customer, cart, meal)
        if created:
            cart.meals.add(cart_meal)
            cart.save()
            return response.Response({"detail": "Meal added to cart", "added": True})
        return response.Response({"detail": "Meal has been added to cart", "added": False},
                                 status=status.HTTP_400_BAD_REQUEST,
                                 )

    @action(methods=['PATCH'],
            detail=False,
            url_path=r'current_customer_cart/change_qty/(?P<qty>\d+)/(?P<cart_meal_id>\d+)',
            )
    def meal_change_qty(self, *args, **kwargs):
        cart_meal = get_object_or_404(CartMeal, id=kwargs['cart_meal_id'])
        cart_meal.qty = int(kwargs['qty'])
        cart_meal.save()
        cart_meal.cart.save()
        return response.Response(status=status.HTTP_200_OK)

    @action(methods=['PUT'], detail=False, url_path=r'current_customer_cart/remove_from_cart/(?P<cart_meal_id>\d+)')
    def meal_remove_from_cart(self, *args, **kwargs):
        cart = self.get_cart(self.request.user)
        cart_meal = get_object_or_404(CartMeal, id=kwargs['cart_meal_id'])
        cart.meals.remove(cart_meal)
        cart_meal.delete()
        cart.save()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['PUT'], detail=False, url_path='current_customer_cart/add_to_order')
    def add_cart_to_order(self, *args, **kwargs):
        cart = Cart.objects.get(owner=self.request.user.customer)
        cart_meals = CartMeal.objects.filter(cart=cart)
        data = self.request.data

        for restaurant, cart_meals in itertools.groupby(CartMeal.objects.filter(cart=cart).order_by('meal__restaurant'),
                                                        lambda s: s.meal.restaurant):
            order = Order.objects.create(
                customer=self.request.user.customer,
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone=data['phone'],
                address=data.get('address', self.request.user.customer.home_address),
                restaurant_address=restaurant.address,
            )

            order.cart_meal.set([cart_meal for cart_meal in cart_meals])

            meals = Meal.objects.filter(
                cartmeal__order=order,
            ).select_related('restaurant')

            for meal in meals:
                send_order_to_restaurant.delay(meal.restaurant.email, meal.title)

        return response.Response({"detail": "Order is created", "added": True})
