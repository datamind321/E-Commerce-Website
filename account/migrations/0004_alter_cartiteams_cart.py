# Generated by Django 4.1.3 on 2022-12-29 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_remove_cart_coupan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartiteams',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_item', to='account.cart'),
        ),
    ]