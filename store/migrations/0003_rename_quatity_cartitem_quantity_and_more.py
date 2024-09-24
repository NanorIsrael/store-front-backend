# Generated by Django 4.2.7 on 2024-09-23 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_cartitem_cart_alter_cartitem_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='quatity',
            new_name='quantity',
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_item', to='store.product'),
        ),
    ]
