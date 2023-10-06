from datetime import datetime
from skidkoman.models import Product, ProductHistory
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from config import settings
from rest_framework.fields import Field


class IntegerToDateField(Field):
    def to_internal_value(self, data):
        try:
            data = int(data)
        except (ValueError, TypeError):
            self.fail('invalid')
        return data

    def to_representation(self, value):
        return (value - datetime.now()).days + 1


class Magic:
    """
    Класс Magic используется для проверки и обновления информации о продукте в базе данных.
    """

    def __init__(self, price, product):
        self.price = price
        self.product = product

    def check_product_history_table(self):
        """
        Функция проверяет, есть ли запись в таблице ProductHistory для данного продукта.
        :return: логическое значение.
        """
        return bool(ProductHistory.objects.filter(product_id=self.product))

    def add_product_history(self):
        """
        Функция add_product_history проверяет, существует ли таблица истории продуктов, и если да,
        то добавляет новую запись с обновленной ценой для данного продукта.
        """
        if self.check_product_history_table():
            exist = ProductHistory.objects.filter(product_id=self.product).last()
            if exist.updated_price == self.price:
                pass
            else:
                ProductHistory.objects.create(product_id=self.product, updated_price=self.price)
                Product.objects.filter(pk=self.product.url).update(current_price=self.price)
        else:
            pass


def send_email(email, context, template=None):
    """
    Функция send_emails отправляет электронное письмо с содержимым HTML на указанный адрес электронной почты.

    :param email:
            Параметр "email"— это адрес электронной почты получателя.

    :param context:
            Параметр "context" — это словарь, содержащий данные, необходимые для отображения шаблона электронной почты.
            Обычно он включает такие переменные, как тема электронного письма, имя получателя и любой другой
            динамический контент, который необходимо включить в электронное письмо.

    :param template:
            Параметр "template" — это имя файла HTML-шаблона, который будет использоваться для создания содержимого
            электронной почты. Этот шаблон должен храниться в каталоге шаблонов вашего проекта.
    """
    html_content = render_to_string(
        template_name=template,
        context=context,
    )

    msg = EmailMultiAlternatives(
        subject=context.get('subject', None),
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()
