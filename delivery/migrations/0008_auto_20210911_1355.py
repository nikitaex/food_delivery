# Generated by Django 3.2.7 on 2021-09-11 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0007_auto_20210911_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='final_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='cart',
            name='meals',
            field=models.ManyToManyField(blank=True, null=True, related_name='related_cart', to='delivery.CartMeal'),
        ),
    ]
