# Generated by Django 4.1.3 on 2023-01-02 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_cart_coupan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartiteams',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='account.cart'),
        ),
    ]