# Generated by Django 3.2.7 on 2021-09-26 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0002_alter_meal_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=9),
        ),
    ]