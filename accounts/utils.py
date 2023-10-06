from templated_mail.mail import BaseEmailMessage
from djoser import utils
from django.contrib.auth.tokens import default_token_generator
from config.settings import EMAIL_CHANGE_CONFIRM_URL


class ChangeEmail(BaseEmailMessage):
    """
    Класс ChangeEmail используется для генерации контекстных данных для шаблона электронной почты для изменения адреса
    электронной почты пользователя.
    """
    template_name = "email/change_email.html"

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = EMAIL_CHANGE_CONFIRM_URL.format(**context)
        return context
