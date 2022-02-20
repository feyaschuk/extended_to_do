# Generated by Django 4.0.2 on 2022-02-19 20:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scheduler', '0002_remove_purchase_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductPurchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_purchases', to='scheduler.recipe', verbose_name='Продукт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_purchases', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'покупку',
                'verbose_name_plural': 'покупки',
                'ordering': ('-date_added',),
            },
        ),
        migrations.AddConstraint(
            model_name='productpurchase',
            constraint=models.UniqueConstraint(fields=('user', 'product'), name='purchase_user_product_unique'),
        ),
    ]