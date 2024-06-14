# Generated by Django 5.0.6 on 2024-06-14 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0021_order_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(blank=True, choices=[(1, 'Pending'), (2, 'Order Placed'), (3, 'Dispatch'), (4, 'On The Way'), (5, 'Delivered'), (6, 'Cancel'), (7, 'Return')], default=1, max_length=100, null=True),
        ),
    ]
