# Generated by Django 5.1.5 on 2025-02-04 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_alter_engraving_upload_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='engraving',
            name='display_id',
            field=models.PositiveIntegerField(default=0, unique=True, verbose_name='ID'),
        ),
    ]
