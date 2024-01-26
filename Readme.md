1) Установка всех зависимостей pip instal -r requirements.txt
2) Создать базу данных posgres
3) Внесение настроек в secret_key.py:

- HOST_USER = Почта с которой будет осуществлятся отпрака
- HOST_PASSWORD = Парольдля почты отправки
- HOST = Сервер отправки

- SUPER_USER = Почта для суперпоользователя
- SUPER_USER_FIRST_NAME = Имя для суперпользователя
- SUPER_USER_LAST_NAME = Фамилия для суперпользователя
- SUPER_USER_PASSWORD = Пароль для суперпользователя

- BD_NAME = Название БД
- BD_USER = Имя пользователя БД

4) Применить миграции python manage.py migrate
5) Создание суперпользователя python manage.py csu
6) Настройка периодичности отправки python manage.py crontab add
6) Запуск сервера python manage.py runserver