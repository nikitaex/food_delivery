# Generated by Django 3.2.7 on 2021-09-19 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0023_auto_20210919_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='description',
            field=models.TextField(default='Complaint on courier <django.db.models.fields.related.ForeignKey>'),
        ),
    ]