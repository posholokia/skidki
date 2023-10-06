from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    Кастомный менеджер модели пользователя для возможности расширения способов регистрации пользователей
    """

    use_in_migrations = True

    def _create_user(self, username=None, email=None, password=None, **extra_fields):
        """
        Создание пользователя
        """

        if not username and not email:
            raise ValueError('Необходимо указать эл. почту!')

        if email:
            email = self.normalize_email(email)

            if not username:
                username = email

        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username=username, email=email, password=password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(
            email=email,
            password=password,
            **extra_fields
        )
