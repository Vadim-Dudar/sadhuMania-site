# Generated by Django 5.1.5 on 2025-02-04 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_engraving'),
    ]

    operations = [
        migrations.AddField(
            model_name='engraving',
            name='upload_at',
            field=models.DateField(editable=False, null=True, verbose_name='Завантажено'),
        ),
    ]
