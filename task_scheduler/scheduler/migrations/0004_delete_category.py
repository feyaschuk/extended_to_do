# Generated by Django 4.0.2 on 2022-02-17 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0003_category_alter_product_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Category',
        ),
    ]
