from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from os.path import join
from colorfield.fields import ColorField
from task_scheduler.settings import MEDIA_ROOT
from users.models import User


class Shop(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название магазина")
    adress = models.CharField(max_length=200, verbose_name="Адрес магазина")
    
    def __str__(self):
        return self.name

class Product(models.Model):
    class Category(models.TextChoices):
        GROCERY = 'grocery'
        HOUSEHOLD = 'household'

    name = models.CharField(max_length=200, verbose_name="Название продукта")
    measurement_unit = models.CharField(max_length=200, verbose_name="Единица измерения")
    image = models.ImageField(upload_to=join(MEDIA_ROOT, "product/"), blank=True, null=True)
    text = models.TextField(verbose_name="Описание продукта")
    category = models.CharField(max_length=200, choices=Category.choices, default=0, verbose_name="Категория продукта")
    adding_date = models.DateField(verbose_name="Дата добавления", auto_now_add=True, db_index=True)
        
    def __str__(self):
        return "{}, {}".format(self.name, self.measurement_unit)


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes", verbose_name="Автор")
    products = models.ManyToManyField(Product, through="ProductRecipe")
    name = models.CharField(max_length=200, verbose_name="Название рецепта")
    image = models.ImageField(upload_to=join(MEDIA_ROOT, "recipes/"), blank=True, null=True)
    video = models.FileField(upload_to=join(MEDIA_ROOT, "video/"), null=True, blank=True)
    text = models.TextField(verbose_name="Текст рецепта")
    cooking_time = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(240)), verbose_name="Время приготовления"
    )
    pub_date = models.DateField(verbose_name="Дата публикации", auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Purchase(models.Model):
    user = models.ForeignKey(User,
        on_delete=models.CASCADE, related_name='product_purchases',
        verbose_name='Покупатель')
    product = models.ForeignKey(Product,
        on_delete=models.CASCADE, related_name='product_purchases',
        verbose_name='Продукт')
    date_added = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата добавления')
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1, message='Не менее 1')],
        verbose_name='Количество продукта'    )   

    class Meta:
        #ordering = ('-date_added',)
        verbose_name = 'покупку продуктов'
        verbose_name_plural = 'покупки продуктов'
        

    def __str__(self):
        return f'Продукт "{self.product}" в списке покупок {self.user}'


class ProductRecipe(models.Model):
    product = models.ForeignKey(Product,
                                   on_delete=models.CASCADE,
                                   related_name='amount',
                                   verbose_name='Ингредиент')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='amount',
                               verbose_name='Рецепт')
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1, message='Не менее 1')],
        verbose_name='Количество ингредиента'
    )

    class Meta:        
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'recipe'],
                name='recipe_product_unique'
            )
        ]
    def __str__(self):
        return f'Ингредиент "{self.product}" рецепта "{self.recipe}".'


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favorite_users', verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorite_recipes', verbose_name='Любимый рецепт')

    class Meta:
        verbose_name = 'Любимые рецепты'
        verbose_name_plural = 'Любимые рецепты'

    def __str__(self):
        return f'{self.user} любит {self.recipe}'


class SchedulerType(models.Model):
    title = models.CharField(verbose_name="Тип задачи", max_length=50, unique=True)
    description = models.TextField(verbose_name="Описание типа задачи", max_length=300, blank=True)
    has_subtask = models.BooleanField(default=False)
    color = ColorField(default="#FFFFFF", unique=True)

    def __str__(self):
        return self.title


class MainTaskScheduler(models.Model):

    class Suit(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5
        SIX = 6

    title = models.CharField(verbose_name="Название задачи", max_length=50)
    description = models.TextField(verbose_name="Краткое описание задачи", max_length=500, blank=True)
    duration = models.DurationField(verbose_name="Ожидаемое время выполнения", blank=True)
    when = models.DateTimeField(blank=True)
    importance = models.IntegerField(choices=Suit.choices, default=0)
    scheduler_type = models.ForeignKey(SchedulerType, blank=True, related_name="Scheduler", on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to=join(MEDIA_ROOT, "scheduler_image/"))
    video = models.FileField(upload_to=join(MEDIA_ROOT, "scheduler_video/"), blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scheduler", verbose_name="Автор")

    def __str__(self):
        return "{}, {}, {}".format(self.title, self.duration, self.when)


class Training(models.Model):
    SMALL = 'S'
    MEDIUM = 'M'
    LARGE = 'L'
    TIMEOUTS = [
        (SMALL, 'Small'),
        (MEDIUM, 'Medium'),
        (LARGE, 'Large'),
    ]
    title = models.CharField(max_length=50, unique=True, verbose_name="Название упражнения")
    duration = models.DurationField(verbose_name="Продолжительность", blank=True)
    count = models.PositiveIntegerField(blank=True)
    timeout = models.CharField(max_length=1, choices=TIMEOUTS, default="S")
    image = models.ImageField(blank=True, upload_to=join(MEDIA_ROOT, "training_image/"))
    video = models.FileField(upload_to=join(MEDIA_ROOT, "training_video/"), blank=True)

    def __str__(self):
        return "{}, {}, {}".format(self.title, self.duration, self.count)
