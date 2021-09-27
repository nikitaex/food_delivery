from decimal import Decimal

from django.core.mail import send_mail


from conf import settings
from delivery.models import Order, CartMeal, Restaurant, Meal, Complaint, Cart, Customer


def send_order_to_restaurant(restaurant_email, meal):
    send_mail(
        'An order has been received',
        f'{meal} \n'
        f'Link to orders: http://127.0.0.1:8000/api/restaurateur/orders',
        settings.EMAIL_HOST_USER,
        [restaurant_email],
        fail_silently=False,
    )


def send_delivery_notification_to_customer(user_email, meal, order_id):
    send_mail(
        'Your order has been delivered',
        f'Your order {meal} has been delivered \n'
        f'If you did not receive the order or you received the wrong order that you ordered, then write a complaint '
        f'to this address within 5 minutes:: http://127.0.0.1:8000/api/omplaint/create_complaint/{order_id}/',
        settings.EMAIL_HOST_USER,
        [user_email],

    )


def get_or_create_cart_meal(user, meal, cart):
    CartMeal.objects.get_or_create(
        user=user,
        meal=meal,
        cart=cart,
    )


def create_order(customer, first_name, last_name, phone, address, restaurant_address):
    Order.objects.create(
        customer=customer,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        address=address,
        restaurant_address=restaurant_address,
    ).save()


def restaurant_create(owner, name, slug, address, email):
    restaurant = Restaurant.objects.create(owner=owner,
                                           name=name,
                                           slug=slug,
                                           address=address,
                                           email=email,
                                           )

    restaurant.save()


def meal_create(title, description, price, restaurant, slug, discount):
    meal = Meal.objects.create(title=title,
                               description=description,
                               price=price,
                               restaurant=restaurant,
                               slug=slug,
                               discount=discount,
                               )
    meal.save()


def create_complaint(order, courier, customer, description):
    Complaint.objects.create(
        order=order,
        courier=courier,
        customer=customer,
        description=description,
    ).save()


def get_cart(user):
    if user.is_authenticated:
        return Cart.objects.get(owner=user.customer, for_anonymous_user=False)
    return Cart.objects.get(for_anonymous_user=True)
