# Generated by Django 4.0.2 on 2022-02-20 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0009_alter_productpurchase_amount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productpurchase',
            options={'verbose_name': 'покупку продуктов', 'verbose_name_plural': 'покупки продуктов'},
        ),
        migrations.AlterModelOptions(
            name='purchase',
            options={'verbose_name': 'покупку', 'verbose_name_plural': 'покупки'},
        ),
    ]