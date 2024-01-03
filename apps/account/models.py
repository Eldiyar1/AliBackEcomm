from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, user_name, password, **extra_fields):

        if not email:
            raise ValueError(_('Необходимо указать адрес электронной почты'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, user_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, user_name, password, **extra_fields)


class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name=_('Адрес электронной почты'))
    user_name = models.CharField(max_length=150, unique=True, verbose_name=_('Имя пользователя'))
    first_name = models.CharField(max_length=150, blank=True, verbose_name=_('Имя'))
    about = models.TextField(max_length=500, blank=True, verbose_name=_('О себе'))
    # Детали доставки
    country = models.CharField(max_length=200, null=True, choices=CountryField().choices + [('', 'Выбрать страну')], )
    phone_number = PhoneNumberField(verbose_name=_('Номер телефона'))
    postcode = models.CharField(max_length=12, blank=True, verbose_name=_('Почтовый индекс'))
    address_line_1 = models.CharField(max_length=150, blank=True, verbose_name=_('Адрес, строка 1'))
    address_line_2 = models.CharField(max_length=150, blank=True, verbose_name=_('Адрес, строка 2'))
    town_city = models.CharField(max_length=150, blank=True, verbose_name=_('Город'))
    # Статус пользователя
    is_active = models.BooleanField(default=False, verbose_name=_('Активен'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Администратор'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'l@1.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.user_name
