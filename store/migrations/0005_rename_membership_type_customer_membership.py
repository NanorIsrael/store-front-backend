# Generated by Django 4.2.7 on 2023-11-21 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_remove_customer_store_custo_last_na_e6a359_idx_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='membership_type',
            new_name='membership',
        ),
    ]
