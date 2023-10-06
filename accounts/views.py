from django.core.cache import cache
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from djoser.serializers import UidAndTokenSerializer
from accounts.serializers import UserEmailSerializer
from .utils import ChangeEmail
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()


class UserEmailChange(viewsets.ModelViewSet):
    """
    Класс UserEmailChange — это набор представлений, который позволяет аутентифицированным пользователям
    изменять свой адрес электронной почты и подтверждать изменение посредством проверки электронной почты.
    """
    queryset = User.objects.all()
    serializer_class = UserEmailSerializer
    permission_classes = [permissions.IsAuthenticated]
    token_generator = default_token_generator

    def get_serializer_class(self):
        if self.action == 'change_email_confirm':
            return UidAndTokenSerializer

        return self.serializer_class

    @action(['post'], detail=False)
    def change_email(self, request, *args, **kwargs):
        """
        Метод принимает от авторизованного пользователя новый адрес email, сериализует данные.
        Если новая почта корректная - вызывает метод send_email_confirm для формирования письма с подтверждением.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        new_email = request.POST.get('email', None)

        if not new_email:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'email': 'Это поле обязательно'})

        elif user.email == new_email:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'email': 'Новая почта совпадает со старой'})

        self.send_email_confirm(user, new_email)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(['post'], detail=False, permission_classes=[permissions.AllowAny])
    def change_email_confirm(self, request, *args, **kwargs):
        """
        Метод получает uid и token пользователя, когда он переходит по ссылке для подтверждения.
        UidAndTokenSerializer по uid и токену определяет пользователя.
        Из кэша по user.id достаем новую почту и перезаписываем ее
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        if user:
            new_email = cache.get(f'user_{user.id}')
            user.change_email(new_email)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def send_email_confirm(self, user, new_email):
        """
        Отправка письма с ссылкой для подтверждения смены email.
        id пользователя и новая почта записываются в кэш для дальнейшего извлечения,
        когда пользователь перейдет по ссылке для подтверждения смены почты
        """
        cache_key = f'user_{user.id}'
        cache.set(cache_key, new_email, timeout=86400)
        context = {"user": user}
        to = [new_email]
        ChangeEmail(self.request, context).send(to)


