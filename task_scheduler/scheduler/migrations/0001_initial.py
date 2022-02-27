# Generated by Django 4.0.2 on 2022-02-27 14:00

import colorfield.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Любимые рецепты',
                'verbose_name_plural': 'Любимые рецепты',
            },
        ),
        migrations.CreateModel(
            name='MainTaskScheduler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название задачи')),
                ('description', models.TextField(blank=True, max_length=500, verbose_name='Краткое описание задачи')),
                ('duration', models.DurationField(blank=True, verbose_name='Ожидаемое время выполнения')),
                ('when', models.DateTimeField(blank=True)),
                ('importance', models.IntegerField(choices=[(1, 'One'), (2, 'Two'), (3, 'Three'), (4, 'Four'), (5, 'Five'), (6, 'Six')], default=0)),
                ('image', models.ImageField(blank=True, upload_to='C:\\Users\\user\\Dev\\extended_to_do\\task_scheduler\\back_media/scheduler_image/')),
                ('video', models.FileField(blank=True, upload_to='C:\\Users\\user\\Dev\\extended_to_do\\task_scheduler\\back_media/scheduler_video/')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название продукта')),
                ('measurement_unit', models.CharField(max_length=200, verbose_name='Единица измерения')),
                ('image', models.ImageField(blank=True, null=True, upload_to='C:\\Users\\user\\Dev\\extended_to_do\\task_scheduler\\back_media/product/')),
                ('text', models.TextField(verbose_name='Описание продукта')),
                ('category', models.CharField(choices=[('grocery', 'Grocery'), ('household', 'Household')], default=0, max_length=200, verbose_name='Категория продукта')),
                ('adding_date', models.DateField(auto_now_add=True, db_index=True, verbose_name='Дата добавления')),
            ],
        ),
        migrations.CreateModel(
            name='ProductRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Не менее 1')], verbose_name='Количество ингредиента')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('amount', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, message='Не менее 1')], verbose_name='Количество продукта')),
            ],
            options={
                'verbose_name': 'покупку продуктов',
                'verbose_name_plural': 'покупки продуктов',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название рецепта')),
                ('image', models.ImageField(blank=True, null=True, upload_to='C:\\Users\\user\\Dev\\extended_to_do\\task_scheduler\\back_media/recipes/')),
                ('video', models.FileField(blank=True, null=True, upload_to='C:\\Users\\user\\Dev\\extended_to_do\\task_scheduler\\back_media/video/')),
                ('text', models.TextField(verbose_name='Текст рецепта')),
                ('cooking_time', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(240)], verbose_name='Время приготовления')),
                ('pub_date', models.DateField(auto_now_add=True, db_index=True, verbose_name='Дата публикации')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='SchedulerType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='Тип задачи')),
                ('description', models.TextField(blank=True, max_length=300, verbose_name='Описание типа задачи')),
                ('has_subtask', models.BooleanField(default=False)),
                ('color', colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=18, samples=None, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название магазина')),
                ('adress', models.CharField(max_length=200, verbose_name='Адрес магазина')),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='Название упражнения')),
                ('duration', models.DurationField(blank=True, verbose_name='Продолжительность')),
                ('count', models.PositiveIntegerField(blank=True)),
                ('timeout', models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')], default='S', max_length=1)),
                ('image', models.ImageField(blank=True, upload_to='C:\\Users\\user\\Dev\\extended_to_do\\task_scheduler\\back_media/training_image/')),
                ('video', models.FileField(blank=True, upload_to='C:\\Users\\user\\Dev\\extended_to_do\\task_scheduler\\back_media/training_video/')),
            ],
        ),
    ]
