# Generated by Django 3.2.7 on 2021-09-09 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0002_rename_cartproduct_cardproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customers_order',
            field=models.ManyToManyField(blank=True, related_name='related_customer', to='delivery.Order'),
        ),
        migrations.AlterField(
            model_name='meal',
            name='restaurant',
            field=models.ManyToManyField(blank=True, to='delivery.Restaurant'),
        ),
    ]