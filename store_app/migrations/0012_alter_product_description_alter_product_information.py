# Generated by Django 5.0.6 on 2024-05-23 14:35

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0011_alter_product_description_alter_product_information'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=tinymce.models.HTMLField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='information',
            field=tinymce.models.HTMLField(null=True),
        ),
    ]
