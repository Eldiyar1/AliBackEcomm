from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomManager(BaseUserManager):
    def create_user(self, email, name, password, **extra_fields):

        if not email:
            raise ValueError(_('Необходимо указать адрес электронной почты'))

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Суперпользователь должен иметь is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Суперпользователь должен иметь is_superuser=True')

        return self.create_user(email, name, password, **extra_fields)
