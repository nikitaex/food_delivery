# Generated by Django 3.2.7 on 2021-09-20 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0028_restaurant_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cart_meal',
            field=models.ManyToManyField(blank=True, to='delivery.CartMeal'),
        ),
    ]
