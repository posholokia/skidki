from django.db import models
from config import settings


class Category(models.Model):
    name = models.CharField('Наименование категории', max_length=64)


class Brand(models.Model):
    name = models.CharField('Наименование бренда', max_length=64)


class Shop(models.Model):
    name = models.CharField('Наименование магазина', max_length=500)


class Product(models.Model):
    title = models.CharField('Наименование товара', max_length=500)
    shop = models.CharField('Интернет-магазин', max_length=500, blank=True)
    description = models.CharField('Описание товара', max_length=5000, blank=True)
    old_price = models.CharField('Цена до скидки', max_length=64, blank=True)
    current_price = models.CharField('Цена со скидкой', max_length=64)
    url = models.URLField('URL товара', unique=True)
    image = models.URLField('URL изображения', blank=True)
    brand = models.CharField('Бренд', max_length=64, blank=True)
    category = models.CharField('Категория', max_length=64, blank=True)
    click_rate = models.IntegerField('Рейтинг кликов', default=0, null=True)

    def get_discount(self):
        if self.old_price and self.current_price:
            return (1 - float(self.current_price) / float(self.old_price)) * 100
        return 0


class ProductHistory(models.Model):
    product_id = models.ForeignKey("Product", on_delete=models.CASCADE)
    last_updated = models.DateTimeField("Последнее обновление цены", auto_now_add=True)
    updated_price = models.CharField("Обновленная цена", max_length=32)


class Request(models.Model):
    TYPE = (
        (0, 'Обо всех изменениях'),
        (1, 'Об увеличении скидки'),
        (2, 'О желаемой скидке'),
    )

    STATUS = (
        (0, 'В работе'),
        (1, 'Выполнен'),
        (2, 'Ошибка в URL'),
        (3, 'Заморожен'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='request')
    email_notification = models.BooleanField('Уведомление на почту', default=False)
    lk_notification = models.BooleanField('Уведомление в личном кабинете', default=False)
    notification_type = models.IntegerField('Тип уведомлений', choices=TYPE, default=0)
    endpoint = models.URLField('Ссылка для отслеживания')
    price = models.IntegerField('Желаемая цена', null=True)
    discount = models.IntegerField('Желаемая скидка', null=True)
    created_at = models.DateField('Дата создания запроса', auto_now_add=True)
    completed_at = models.DateField('Дата завершения запроса', default=None, null=True)
    period_date = models.DateTimeField('Время отслеживания', auto_now_add=True)
    status = models.IntegerField('Статус запроса', choices=STATUS, default=0)


class Notifications(models.Model):
    request = models.ForeignKey('Request', on_delete=models.CASCADE, related_name='notification')
    text = models.CharField('Сообщение', max_length=256)
    created_at = models.DateField(auto_now_add=True)
