# Generated by Django 3.2.7 on 2021-09-18 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0015_auto_20210917_1934'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='cart_meals',
            new_name='cart_meal',
        ),
    ]
