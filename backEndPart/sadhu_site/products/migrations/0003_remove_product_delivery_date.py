# Generated by Django 5.1.5 on 2025-05-27 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_order_deadline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='delivery_date',
        ),
    ]
