# Generated by Django 4.2.7 on 2023-11-21 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_rename_quatity_orderitem_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='Order',
            new_name='order_id',
        ),
    ]
