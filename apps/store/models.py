from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(verbose_name=_("Название категории"), help_text=_("Обязательно и уникально"),
                            max_length=255, unique=True)
    slug = models.SlugField(verbose_name=_("URL категории"), max_length=255, unique=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children",
                            verbose_name=_("Родительская категория"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активный"))

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")

    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(verbose_name=_("Название типа продукта"), help_text=_("Обязательно"), max_length=255,
                            unique=True)
    is_active = models.BooleanField(default=True, verbose_name=_("Активность"))

    class Meta:
        verbose_name = _("Тип продукта")
        verbose_name_plural = _("Типы продуктов")

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT, verbose_name=_("Тип продукта"))
    name = models.CharField(verbose_name=_("Характеристика типа продукта"), help_text=_("Обязательно"), max_length=255)

    class Meta:
        verbose_name = _("Характеристика продукта")
        verbose_name_plural = _("Характеристики продуктов")

    def __str__(self):
        return self.name


class Product(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT, verbose_name=_("Тип продукта"))
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, verbose_name=_("Категория"))
    title = models.CharField(verbose_name=_("Заголовок"), help_text=_("Обязательно"), max_length=255, )
    description = models.TextField(verbose_name=_("Описание"), help_text=_("Не обязательно"), blank=True)
    slug = models.SlugField(max_length=255, verbose_name=_("URL продукта"))
    regular_price = models.DecimalField(
        verbose_name=_("Обычная цена"),
        help_text=_("Максимум 999.99"),
        error_messages={"name": {"max_length": _("Цена должна быть от 0 до 999.99."), }, },
        max_digits=5,
        decimal_places=2)
    discount_price = models.DecimalField(
        verbose_name=_("Цена со скидкой"),
        help_text=_("Максимум 999.99"),
        error_messages={"name": {"max_length": _("Цена должна быть от 0 до 999.99."), }, },
        max_digits=5,
        decimal_places=2)
    is_active = models.BooleanField(verbose_name=_("Активный"), help_text=_("Изменить видимость продукта"),
                                    default=True)
    created_at = models.DateTimeField(_("Создано"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Обновлено"), auto_now=True)
    users_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_wishlists", blank=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Продукт")
        verbose_name_plural = _("Продукты")

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])

    def __str__(self):
        return self.title


class ProductSpecificationValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Продукт"))
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT, verbose_name=_("Характеристика"))
    value = models.CharField(
        verbose_name=_("Значение"),
        help_text=_("Значение характеристики продукта (максимум 255 слов)"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("Значение характеристики продукта")
        verbose_name_plural = _("Значения характеристик продуктов")

    def __str__(self):
        return self.value


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images",
                                verbose_name=_("Продукт"))
    image = models.ImageField(
        verbose_name=_("Изображение"),
        help_text=_("Загрузите изображение продукта"),
        upload_to="images/",
        default="images/default.png",
    )
    alt_text = models.CharField(
        verbose_name=_("Альтернативный текст"),
        help_text=_("Пожалуйста, добавьте альтернативный текст"),
        max_length=255,
        null=True,
        blank=True,
    )
    is_feature = models.BooleanField(default=False, verbose_name=_("Главная"))
    created_at = models.DateTimeField(_("Создано"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Обновлено"), auto_now=True)

    class Meta:
        verbose_name = _("Изображение продукта")
        verbose_name_plural = _("Изображения продуктов")

    def __str__(self):
        return str(self.product)
