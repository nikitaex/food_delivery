# Generated by Django 3.2.7 on 2021-09-17 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0013_auto_20210916_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='discount',
            field=models.IntegerField(default=0),
        ),
    ]
