# Generated by Django 4.0.2 on 2022-02-20 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0007_alter_productpurchase_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productrecipe',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amount', to='scheduler.product', verbose_name='Ингредиент'),
        ),
        migrations.AlterField(
            model_name='productrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amount', to='scheduler.recipe', verbose_name='Рецепт'),
        ),
    ]