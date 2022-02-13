from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        max_length=100, unique=True,
        blank=True, verbose_name='Username пользователя')
    email = models.EmailField(
        blank=True, unique=True, verbose_name='mail пользователя')
    first_name = models.CharField(
        max_length=100, verbose_name='Имя пользователя')
    last_name = models.CharField(
        max_length=100, verbose_name='Фамилия пользователя')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
