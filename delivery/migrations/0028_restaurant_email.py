# Generated by Django 3.2.7 on 2021-09-20 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0027_alter_order_courier'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='email',
            field=models.EmailField(default=2, max_length=254),
            preserve_default=False,
        ),
    ]
