# Generated by Django 4.2.7 on 2024-09-23 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_collection_options_alter_product_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='featured_product',
        ),
        migrations.RemoveField(
            model_name='product',
            name='promotions',
        ),
    ]
