# Generated by Django 5.1.5 on 2025-01-21 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_length_alter_product_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sale_price',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=11, null=True, verbose_name='Акційна ціна'),
        ),
    ]
