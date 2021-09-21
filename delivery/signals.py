from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from delivery.models import Customer, Cart

User = get_user_model()


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):

    if created:
        Customer.objects.create(user=instance)


@receiver(post_save, sender=Customer)
def create_cart(sender, instance, created, **kwargs):

    if created:
        Cart.objects.create(owner=instance)
