from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    GENDER = (
        ('M', 'Мужчина'),
        ('W', 'Женщина')
    )
    username = models.CharField('Логин', max_length=150, blank=True)
    email = models.EmailField('Эл. почта', null=True)
    date_joined = models.DateTimeField('Дата создания', auto_now_add=True)
    is_active = models.BooleanField('Активирован', default=True)  # обязательно
    is_staff = models.BooleanField('Персонал', default=False)  # для админ панели

    # заполняемые данные в профиле:
    phone = models.CharField('Номер телефона', max_length=30, blank=True)
    first_name = models.CharField('Имя', max_length=32, null=True)
    last_name = models.CharField('Фамилия', max_length=32, null=True)
    age = models.IntegerField('Возраст', null=True)
    gender = models.CharField('Пол', choices=GENDER, max_length=1, blank=True)
    city = models.CharField('Город', max_length=32, blank=True)
    description_user = models.CharField('О себе', max_length=512, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def change_email(self, new_email):
        if new_email:
            self.email = new_email
            self.username = self.email
            self.save()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        unique_together = ['email', 'username']  # связка email+username уникальна
