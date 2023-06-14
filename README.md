# LinkUp

# Описание проекта

LinkUp - это приложение социальной сети, которое предоставляет функциональность подписок, публикации постов, обмена сообщениями, лайков и комментариев. Проект разработан с использованием следующих зависимостей: Python 3, PostgreSQL, Django (последние версии), JavaScript, HTML и CSS. Для работы с проектом необходимо настроить переменные окружения, описанные ниже, и выполнить указанные последовательности действий.

# Как поднять локально проект?

Зависимости:

Python 3

PostgreSQL

Django

JavaScript

HTML

CSS

# Переменные окружения для продакшена, для локальной разработки можно и не указывать:

| Key    | Description   |    Default value  |
| :---         |     :---      |          :--- |
| `DJANGO_SECRET_KEY`  | Секретный ключ  | secret-key              |
| `DJANGO_DEBUG`  | Режим отладки True или False  | True              |
| `DJANGO_ALLOWED_HOST`| Разрешенный хост | 0.0.0.0,127.0.0.1 |
| `DEFAULT_DATABASE_URL`  | postgres://user:password@host:port/database_name | postgres://postgres:postgres@db:5432/socialnetworkdb |

# Последовательность действий

    $ git clone https://github.com/JustSultan/final-project2

    $ cd linkup/

    $ virtualenv venv

    $ pip install -r requirements.txt

Необходимо создать базу данных PostgreSQL:

    $ sudo -u postgres psql

    $ create database socialnetworkdb encoding 'UTF-8';

    $ \q

После создания базы данных необходимо выполнить миграцию и запустить тестовый сервер:

    $ python manage.py migrate

    $ python manage.py runserver

Если все прошло успешно, вы можете открыть проект по ссылке http://localhost:8000 и начать его использование.






