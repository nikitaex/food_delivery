from django.utils import timezone

from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from django.shortcuts import get_object_or_404

from delivery.premissions import RestaurateurOnly, CourierOnly
from delivery.tasks import send_delivery_notification_to_customer
from .serializers import RestaurantSerializer, MealSerializer
from ..cart.serializers import OrderSerializer, ComplaintSerializer
from delivery.models import Meal, Restaurant, Order
from ...service import restaurant_create, meal_create, create_complaint


class RestaurantViewSet(ModelViewSet):
    serializer_class = RestaurantSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        if self.request.user.is_restaurateur:
            queryset = Restaurant.objects.filter(owner=self.request.user)
            return queryset
        queryset = Restaurant.objects.all()
        return queryset

    def get_permissions(self):
        method = self.request.method
        if method == 'POST' or method == 'PATCH':
            return [RestaurateurOnly()]
        else:
            return [AllowAny()]

    @action(['POST'], detail=False, url_path='create_restaurant')
    @permission_classes([RestaurateurOnly])
    def create_restaurant(self, *args, **kwargs):
        restaurant_data = self.request.data
        serializer = self.get_serializer(restaurant_data)

        restaurant_create(owner=self.request.user,
                          name=serializer["name"].value,
                          slug=serializer["slug"].value,
                          address=serializer["address"].value,
                          email=serializer["email"].value,
                          )

        return Response(status=HTTP_201_CREATED)

    @action(['GET'], detail=False, url_path='orders')
    def restaurant_orders(self, *args, **kwargs):
        restaurant = Restaurant.objects.get(owner=self.request.user)
        order = Order.objects.filter(cart_meal__meal__restaurant=restaurant)

        serializer = OrderSerializer(order, many=True)

        return Response(serializer.data)

    @action(methods=['PATCH'],
            detail=False,
            url_path=r'orders/accepted_for_cooking/(?P<order_id>\d+)',
            )
    def order_change_status_on_accepdet(self, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['order_id'])
        order.status = order.STATUS_ACCEPTED
        order.save()
        return Response(status=HTTP_200_OK)

    @action(methods=['PATCH'],
            detail=False,
            url_path=r'orders/cooked/(?P<order_id>\d+)',
            )
    def order_change_status_on_cooked(self, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['order_id'])
        order.status = order.STATUS_COOKED
        order.save()
        return Response(status=HTTP_200_OK)

    @action(['GET'], detail=False, url_path='orders')
    def restaurant_orders(self, *args, **kwargs):
        restaurant = Restaurant.objects.get(owner=self.request.user)
        order = Order.objects.filter(cart_meal__meal__restaurant=restaurant)

        serializer = OrderSerializer(order, many=True)

        return Response(serializer.data)

    @action(methods=['PATCH'],
            detail=False,
            url_path=r'orders/accepted_for_cooking/(?P<order_id>\d+)',
            )
    def order_change_status_on_accepted(self, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['order_id'])
        order.status = order.STATUS_ACCEPTED
        order.save()
        return Response(status=HTTP_200_OK)

    @action(methods=['PATCH'],
            detail=False,
            url_path=r'orders/cooked/(?P<order_id>\d+)',
            )
    def order_change_status_on_cooked(self, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['order_id'])
        order.status = order.STATUS_COOKED
        order.save()
        return Response(status=HTTP_200_OK)


class MealViewSet(ModelViewSet):
    serializer_class = MealSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        if self.request.user.is_restaurateur:
            queryset = Meal.objects.filter(restaurant=Restaurant.objects.filter(owner=self.request.user))
            return queryset
        return Meal.objects.all()

    def get_permissions(self):
        method = self.request.method
        if method == 'POST' or method == 'PUT' or method == 'PATCH':
            return [RestaurateurOnly()]
        else:
            return [AllowAny()]

    @action(['POST'], detail=False, url_path='create_meal')
    def create_meal(self, *args, **kwargs):
        meal_data = self.request.data
        restaurant = Restaurant.objects.get(owner=self.request.user)
        serializer = MealSerializer(meal_data)

        meal_create(title=serializer["title"].value,
                    description=serializer["description"].value,
                    price=serializer["price"].value,
                    restaurant=restaurant,
                    slug=serializer["slug"].value,
                    discount=serializer["discount"].value,
                    )

        return Response(status=HTTP_201_CREATED)

    @action(['PUT'], detail=False, url_path=r'remove_meal/(?P<meal_slug>\w+)')
    def remove_meal(self, *args, **kwargs):
        meal = get_object_or_404(Meal, slug=kwargs['meal_slug'])
        meal.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(['PUT'], detail=False, url_path=r'change_meal/(?P<meal_slug>\w+)')
    def change_meal(self, *args, **kwargs):
        meal = get_object_or_404(Meal, slug=kwargs['meal_slug'])
        data = self.request.data

        restaurant = Restaurant.objects.get(owner=self.request.user)
        meal.restaurant = restaurant
        meal.title = data.get('title', meal.title)
        meal.description = data.get('description', meal.description)
        meal.price = data.get('price', meal.price)
        meal.slug = data.get('slug', meal.slug)
        meal.discount = data.get('discount', meal.discount)

        meal.save()
        serializer = MealSerializer(meal)
        return Response(serializer.data, status=HTTP_200_OK)


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.filter(status='cooked')
    permission_classes = (CourierOnly,)

    @action(methods=['GET'], detail=False, url_path='current_courier_orders')
    def get_current_courier_orders(self, *args, **kwargs):
        orders = Order.objects.filter(courier=self.request.user)

        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data)

    @action(methods=['PUT'], detail=False, url_path=r'take_order/(?P<order_id>\d+)')
    def get_orders(self, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['order_id'])
        order.courier = self.request.user.courier
        order.status = order.STATUS_ACCEPTED_BY_COURIER
        order.save()
        return Response(status=HTTP_200_OK)

    @action(methods=['PUT'], detail=False, url_path=r'deliver_order/(?P<order_id>\d+)')
    def deliver_order(self, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['order_id'])
        order.status = order.STATUS_DELIVERED
        order.delivered_at = timezone.now()
        order.save()

        meals = Meal.objects.filter(cartmeal__order=order)
        meals_list = []
        for meal in meals:
            meals_list.append(f"{meal.title},")

        send_delivery_notification_to_customer.delay(order.customer.user.email, " ".join(meals_list), order_id=order.id)

        return Response(status=HTTP_200_OK)


class ComplaintViewSet(ModelViewSet):
    serializer_class = ComplaintSerializer
    queryset = Order.objects.all()

    @action(methods=['POST'], detail=False, url_path=r'create_complaint/(?P<order_id>\d+)')
    def create_complaint(self, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['order_id'])
        description = self.request.data
        time_difference = (timezone.now()-order.delivered_at).seconds
        if time_difference <= 300:
            complaint = create_complaint(
                order=order,
                courier=order.courier,
                customer=order.customer,
                description=description.get('description'),
            )
            complaint.save()

            serializer = ComplaintSerializer(complaint)

            return Response(serializer.data, status=HTTP_200_OK)
        return Response(
            {"detail": "A complaint cannot be created. It has been more than 5 minutes since the delivery."},
            status=HTTP_204_NO_CONTENT,
        )
