# Generated by Django 4.0.2 on 2022-02-20 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0010_alter_productpurchase_options_alter_purchase_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='productpurchase',
            name='purchase',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='product_purchases', to='scheduler.purchase', verbose_name='Покупки из рецептов'),
            preserve_default=False,
        ),
    ]
