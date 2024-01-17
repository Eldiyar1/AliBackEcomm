import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.account.managers import CustomManager


class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name=_('Адрес электронной почты'))
    name = models.CharField(max_length=150, blank=True, verbose_name=_('Имя'))
    mobile = PhoneNumberField(verbose_name=_('Номер телефона'))
    is_active = models.BooleanField(default=False, verbose_name=_('Активен'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Администратор'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))

    objects = CustomManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"

    def email_user(self, subject, message):
        send_mail(subject, message, 'l@1.com', [self.email], fail_silently=False)

    def __str__(self):
        return self.name


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, verbose_name=_("Покупатель"), on_delete=models.CASCADE)
    full_name = models.CharField(verbose_name=_("Полное имя"), max_length=150)
    phone = PhoneNumberField(verbose_name=_('Номер телефона'))
    postcode = models.CharField(max_length=12, blank=True, verbose_name=_('Почтовый индекс'))
    address_line_1 = models.CharField(max_length=150, blank=True, verbose_name=_('Адрес, строка 1'))
    address_line_2 = models.CharField(max_length=150, blank=True, verbose_name=_('Адрес, строка 2'))
    town_city = models.CharField(max_length=150, blank=True, verbose_name=_('Город'))
    delivery_instructions = models.CharField(max_length=255, verbose_name=_("Инструкции по доставке"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Создано"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Обновлено"))
    default = models.BooleanField(default=False, verbose_name=_("По умолчанию"))

    class Meta:
        verbose_name = _("Адрес")
        verbose_name_plural = _("Адреса")

    def __str__(self):
        return f"{self.full_name}, {self.address_line_1}, {self.town_city}"

