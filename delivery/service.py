from django.core.mail import send_mail


from conf import settings


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
