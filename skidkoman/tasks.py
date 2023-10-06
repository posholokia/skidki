from datetime import datetime
from django.db.models import Q
from django.core import management
from celery import shared_task
from .models import Request, Product, Notifications
from scraper.scraper.spiders.request_search import ByUserRequest
from .utils import Magic, send_email


@shared_task
def week_update():
    management.call_command('runspider')


@shared_task
def task_monitor():
    """
    Функция task_monitor отслеживает товары по url которые задали пользователи в своих запросах.
    """
    date_now = datetime.now()
    tracking_requests = Request.objects.filter(status=0, period_date__gte=date_now).values('endpoint').distinct()
    for url in tracking_requests:
        scraper = ByUserRequest(url['endpoint'])
        price = scraper.getting_price()
        product = Product.objects.get(url=url['endpoint'])
        abracadabra = Magic(price, product)
        abracadabra.add_product_history()



@shared_task
def time_end_notification():
    """
    Периодическая задача, проверяет истечение срока отслеживания, направляет пользователям уведомление и меняет
    статус запроса на "Завершен"
    """
    date_now = datetime.now()
    end_requests = (
        Request.objects.filter(period_date__isnull=False, status=0).filter(period_date__lt=date_now)
    )

    request_notification = (end_requests.filter(Q(email_notification=True) | Q(lk_notification=True))
                            .select_related('user', 'product')
                            .only('user__email', 'product__title', 'email_notification', 'lk_notification'))

    notifications = []

    for request in request_notification:
        email = request.user.email if request.email_notification else None
        request_id = request.id if request.lk_notification else None
        title = request.product.title

        text = (f'Срок отслеживания товара {title} подошел к концу. Вы можете продлить срок '
                f'отслеживания или товар {title} переместится в Архив.')

        if email:
            template_name = 'email/end_time_tracker.html'
            email = request.user.email
            context = {
                'title': request.product.title,
                'subject': 'Тема письма'
            }
            send_email(email, context, template=template_name)

        if request_id:
            notifications.append(Notifications(request_id=request_id, text=text))

    request_notification.update(status=1)
    Notifications.objects.bulk_create(notifications)


@shared_task
def create_email_notification(emails, title, discount, difference_discount, about):
    """
    Подготовка данных для email уведомления и запуск функции отправки почты
    context: контекст html шаблона письма
    """
    context = {
        'title': title,
        'discount': discount,
        'difference_discount': difference_discount,
        'notifi_type': about,
        'subject': 'Тема письма'
    }

    if about == 'find':
        template_name = 'email/success_request.html'

    elif about == 'changed':
        template_name = 'email/discount_up.html'

    for email in emails:
        send_email(email, context, template=template_name)


@shared_task
def create_lk_notification(lk_ids, title, discount, difference_discount, about):
    """
    Формирует список объектов Notifications и одним запросом сохраняет их все в БД
    """
    if about == 'find':
        text = (f'Скидка на товар {title} увеличилась до желаемой {discount}%. Вы можете перейти '
                f'в магазин и купить товар.')

    elif about == 'changed':
        text = (f'Скидка на товар {title} увеличилась на {difference_discount}%. Вы можете перейти на '
                f'страницу магазина и купить товар {title} или дождаться повышения скидки до желаемой.')

    notifications = []

    for request_id in lk_ids:
        notifications.append(Notifications(request_id=request_id, text=text))

    Notifications.objects.bulk_create(notifications)
