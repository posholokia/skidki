## Установка:

1. Клонируйте репозиторий на свой компьютер
2. Установите и активируйте виртуальное виртуальное окружение в папке с проектом:

```
python3 -m venv venv
source venv/bin/activate
```

3. Установите зависимости:

```
pip install -r requirements.txt
```

4. Создайте и примените миграции

   **ВАЖНО**: сперва выполнить команду:

   `python3 manage.py makemigrations`

   только после этого:

   `python3 manage.py migrate`

5. Создайте суперпользователя:

   `python3 manage.py createsuperuser`

   Укажите email, firstname, lastname и пароль для суперюзера.

6. Запуск сервера:

   http:

   `python3 manage.py runserver`

## Настройка OAuth.

1. Перейдите в админ панель http://127.0.0.1:8000/admin/ и войдите под суперпользователем.

2. В разделе DJANGO OAUTH TOOLKIT - Applications создайте 3 приложения:

    - поля **Client id**, **Client secret**, не трогать;

      **Client id** и **Client secret** должен знать фронтэнд для направления запроса на сервер.

      **ВАЖНО!!!** **Client secret** нужно скопировать себе до сохранения приложения, после создания приложения он будет
      захеширован.

      Если **Client secret** не был скопирован, нужно пересоздать приложение и скопировать его до сохранения приложения.

    - поля **Redirect uris** и **Post logout redirect uris** оставить пустыми;

    - в поле **User** выбрать ранее созданного суперюзера из списка;

    - **Client type** установить *Confidential*;

    - **Authorization grant** type установить *Resource owner password-based*;

    - **Name** (опционально) - Yandex, Google, VKontakte, в соответствии с OAuth провайдерами.

      Каждое созданное приложение будет регистрировать/аутентифицировать пользователей и выдавать токены доступа. Одно
      приложение может работать только с одним провайдером.


## Переменные окружения
**Подключение к БД Postgres**
```
NAME = название БД
USER = имя пользователя
PASSWORD = пароль
HOST = хост
PORT = порт
```
**EMAIL хостинг**
```
EMAIL_HOST_USER = адрес почты
EMAIL_HOST_PASSWORD = пароль почты
```
**Oauth2 авторизация**
```angular2html
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = Client ID приложения гугл
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = Client secret приложения гугл

SOCIAL_AUTH_VK_OAUTH2_KEY = ID приложения ВК
SOCIAL_AUTH_VK_OAUTH2_SECRET = Защищённый ключ ВК

SOCIAL_AUTH_YANDEX_OAUTH2_KEY = ClientID приложения яндекс
SOCIAL_AUTH_YANDEX_OAUTH2_SECRET = Client secret приложения яндекс
```

## Запуск периодических задач
`celery -A config worker -l INFO -B --concurrency=4
`
## API Documentation.

    Swagger UI: `http://127.0.0.1:8000/swagger/` 
    Yaml: `http://127.0.0.1:8000/swagger.yaml/` 
    JSON: `http://127.0.0.1:8000/swagger.json/` 
