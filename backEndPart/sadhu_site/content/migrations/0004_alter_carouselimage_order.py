# Generated by Django 5.1.5 on 2025-01-21 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_carouselimage_slide_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carouselimage',
            name='order',
            field=models.PositiveIntegerField(default=0, unique=True, verbose_name='Порядок відображення'),
        ),
    ]
