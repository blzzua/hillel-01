# Generated by Django 4.1.7 on 2023-03-29 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0009_order_total_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='Discount',
            new_name='discount_id',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='Item_ID',
            new_name='item_id',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='DiscountPrice',
            new_name='item_price',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='Order_ID',
            new_name='order_id',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='ItemPrice',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='discount_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=18),
            preserve_default=False,
        ),
    ]
