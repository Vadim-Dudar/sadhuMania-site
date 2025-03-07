# Generated by Django 5.1.5 on 2025-01-21 10:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='length',
            field=models.IntegerField(default=14, validators=[django.core.validators.MinValueValidator(14)], verbose_name='Ширина'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=11, verbose_name='Ціна'),
        ),
        migrations.AlterField(
            model_name='product',
            name='sale_price',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=11, null=True, verbose_name='Ціна'),
        ),
        migrations.AlterField(
            model_name='product',
            name='width',
            field=models.IntegerField(default=35, validators=[django.core.validators.MinValueValidator(20)], verbose_name='Довжина'),
        ),
    ]
