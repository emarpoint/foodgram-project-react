
### :hammer_and_wrench: Стек технологий:


[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

<div>
    <img src="https://github.com/devicons/devicon/blob/master/icons/docker/docker-original-wordmark.svg" title="Docker" alt="Docker" width="40" height="40"/>&nbsp;
</div>

# Проект Foodgram
*https://github.com/emarpoint/foodgram-project-react*


## Описание

Cайт Foodgram - онлайн-сервис, на котором пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд. Проект использует базу данных PostgreSQL. Проект запускается в трёх контейнерах (nginx, PostgreSQL и Django) (контейнер frontend используется лишь для подготовки файлов) через docker-compose на сервере. Образ с проектом загружается на Docker Hub.
![foodgram-main](image_for_readme/22766.jpg)



## Пользовательские роли

### Гость (неавторизованный пользователь)

Что могут делать неавторизованные пользователи:

- Создать аккаунт.
- Просматривать рецепты на главной.
- Просматривать отдельные страницы рецептов.
- Просматривать страницы пользователей.
- Фильтровать рецепты по тегам.

### Авторизованный пользователь

Что могут делать авторизованные пользователи:

- Входить в систему под своим логином и паролем.
- Выходить из системы (разлогиниваться).
- Менять свой пароль.
- Создавать/редактировать/удалять собственные рецепты
- Просматривать рецепты на главной.
- Просматривать страницы пользователей.
- Просматривать отдельные страницы рецептов.
- Фильтровать рецепты по тегам.
- Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов.
- Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл со количеством необходимых ингридиентов для рецептов из списка покупок.
- Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок.

### Администратор

Администратор обладает всеми правами авторизованного пользователя. Плюс к этому он может:

- изменять пароль любого пользователя,
- создавать/блокировать/удалять аккаунты пользователей,
- редактировать/удалять любые рецепты,
- добавлять/удалять/редактировать ингредиенты.
- добавлять/удалять/редактировать теги.


## Ресурсы API Foodgram

- Ресурс auth: аутентификация.
- Ресурс users: пользователи.
- Ресурс tags: получение данных тега или списка тегов рецепта.
- Ресурс recipes: создание/редактирование/удаление рецептов, а также получение списка рецептов или данных о рецепте.
- Ресурс shopping_cart: добавление/удаление рецептов в список покупок.
- Ресурс download_shopping_cart: cкачать файл со списком покупок.
- Ресурс favorite: добавление/удаление рецептов в избранное пользователя.
- Ресурс subscribe: добавление/удаление пользователя в подписки.
- Ресурс subscriptions: возвращает пользователей, на которых подписан текущий пользователь. В выдачу добавляются рецепты.
- Ресурс ingredients: получение данных ингредиента или списка ингредиентов.


 ## Установка

В приложения настроено Continuous Integration и Continuous Deployment:
- автоматический запуск тестов,
- обновление образов на Docker Hub,
- автоматический деплой на боевой сервер при пуше в главную ветку main.


## Шаблон наполнения env-файла

DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 


## Создание образа

Запустите терминал. Убедитесь, что вы находитесь в той же директории, где сохранён Dockerfile, и запустите сборку образа:
docker build -t foodgram .  
build — команда сборки образа по инструкциям из Dockerfile.
-t foodgram — ключ, который позволяет задать имя образу, а потом и само имя.
. — точка в конце команды — путь до Dockerfile, на основе которого производится сборка..


## Развёртывание проекта в нескольких контейнерах

Инструкции по развёртыванию проекта в нескольких контейнерах пишут в файле docker-compose.yaml. 
Убедитесь, что вы находитесь в той же директории, где сохранён docker-compose.yaml и запустите docker-compose командой docker-compose up. У вас развернётся проект, запущенный через Gunicorn с базой данных Postgres.


## Стек технологий

- asgiref==3.5.0
- autopep8==1.6.0
- certifi==2021.10.8
- cffi==1.15.0
- charset-normalizer==2.0.12
- coreapi==2.3.3
- coreschema==0.0.4
- cryptography==36.0.1
- defusedxml==0.7.1
- Django==2.2.19
- django-colorfield==0.6.3
- django-extra-fields==3.0.2
- django-filter==21.1
- django-rest-framework==0.1.0
- django-templated-mail==1.1.1
- djangorestframework==3.13.1
- djoser==2.1.0
- flake8==4.0.1
- idna==3.3
- importlib-metadata==1.7.0
- itypes==1.2.0
- Jinja2==3.0.3
- MarkupSafe==2.1.0
- mccabe==0.6.1
- oauthlib==3.2.0
- Pillow==9.0.1
- psycopg2-binary==2.8.6
- pycodestyle==2.8.0
- pycparser==2.21
- pyflakes==2.4.0
- PyJWT==2.3.0
- python-dotenv==0.19.2
- python3-openid==3.2.0
- pytz==2021.3
- reportlab==3.6.9
- requests==2.27.1
- requests-oauthlib==1.3.1
- six==1.16.0
- social-auth-app-django==4.0.0
- social-auth-core==4.2.0
- sqlparse==0.4.2
- toml==0.10.2
- typing_extensions==4.1.1
- uritemplate==4.1.1
- urllib3==1.26.8
- zipp==3.7.0
- gunicorn==20.0.4


## Примеры

Примеры запросов по API:

- [GET] /api/users/ - Получить список всех пользователей.
- [POST] /api/users/ - Регистрация пользователя.
- [GET] /api/tags/ - Получить список всех тегов.
- [POST] /api/recipes/ - Создание рецепта.
- [GET] /api/recipes/download_shopping_cart/ - Скачать файл со списком покупок.
- [POST] /api/recipes/{id}/favorite/ - Добавить рецепт в избранное.
- [DEL] /api/users/{id}/subscribe/ - Отписаться от пользователя.
- [GET] /api/ingredients/ - Список ингредиентов с возможностью поиска по имени.


### Автор: *Марецкий Е.*
*https://github.com/emarpoint*


