from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import Q
from .tasks import create_email_notification, create_lk_notification
from .models import Product


@receiver(pre_save, sender=Product)
def check_notification(sender, instance, **kwargs):
    """
    Функция представляет собой приемник сигнала предварительного сохранения в Python, который проверяет
    изменения в объекте Product и создает уведомления о задачах на основе определенных условий.

    :param sender:
        Параметр sender относится к классу модели, отправляющему сигнал.
        В данном случае это модель «Продукт».

    :param instance:
        Параметр «instance» относится к сохраняемому экземпляру модели «Product».
        Он представляет объект, который создается или обновляется.
    """
    if not instance._state.adding:  # проверка, что объект изменен, а не создан
        product = Product.objects.get(pk=instance.pk)
        discount = instance.get_discount()
        old_discount = product.get_discount()
        difference_discount = discount - old_discount
        price = instance.current_price
        title = instance.title

        success_requests = (instance.request.filter(status=0)
                            .filter(Q(discount__lte=discount) | Q(price__gte=price))
                            .filter(Q(notification_type=0) | Q(notification_type=2)))

        if success_requests.exists():
            create_task_notification(success_requests, title, discount, difference_discount, 'find')

        if difference_discount > 0:
            discount_up_request = (instance.request.filter(status=0)
                                   .filter(Q(notification_type=0) | Q(notification_type=1))
                                   .exclude(Q(discount__lte=discount) | Q(price__gte=price)))

            if discount_up_request.exists():
                create_task_notification(discount_up_request, title, discount, difference_discount, 'changed')


def create_task_notification(qs, title, discount, difference_discount, about):
    """
    Функция create_task_notification отправляет уведомления пользователям на основе их предпочтений.

    :param qs:
        Набор запросов, содержащий отправляемые уведомления

    :param title:
        Название задачи или уведомления

    :param discount:
        Параметр «скидка» — это сумма скидки на уведомление о задаче

    :param difference_discount:
        Параметр «difference_discount» используется для представления разницы в скидке между текущей задачей и
        предыдущей задачей. Это числовое значение, которое указывает, насколько изменилась скидка.

    :param about:
        Параметр «about» — это описание или информация о создаваемой задаче/уведомлении
    """
    request_notifications = (qs.filter(Q(email_notification=True) | Q(lk_notification=True))
                             .select_related('user', 'product')
                             .only('user__email', 'product__title', 'email_notification', 'lk_notification'))

    emails = []
    lk_ids = []

    for request in request_notifications:
        email = request.user.email if request.email_notification else None
        request_id = request.id if request.lk_notification else None

        if email:
            emails.append(email)

        if request_id:
            lk_ids.append(request_id)

    if emails:
        create_email_notification.apply_async((emails, title, discount, difference_discount, about))

    if lk_ids:
        create_lk_notification.apply_async((lk_ids, title, discount, difference_discount, about))

    request_notifications.update(status=1)
