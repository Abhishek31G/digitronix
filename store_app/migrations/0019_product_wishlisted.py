# Generated by Django 5.0.6 on 2024-06-05 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0018_orderitem_user_alter_order_additional_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='wishlisted',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
