### Лабораторная работа №2 и №3. Савва Даниил

#

Настройка для подключения к базы данных postgresql находится в файле internal/data/ApplicationDbContext.py. В проекте используется библиотека alembic и создана миграция, чтобы обновить содержание таблицы базы данных, выполните в корне проекта команду через консоль:

#

alembic upgrade head

#

Проверка на существование мастер-пользователя происходит автоматически при каждом запуске