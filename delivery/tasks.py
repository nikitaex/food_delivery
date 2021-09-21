from celery import app

from .service import send_order_to_restaurant, send_delivery_notification_to_customer


@app.shared_task
def send_order_to_restaurant(restaurant_email, meal):
    send_order_to_restaurant(restaurant_email, meal)


@app.shared_task
def send_delivery_notification_to_customer(user_email, meal, order_id):
    send_delivery_notification_to_customer(user_email, meal, order_id)
