#  Foodgram - сохрани рецепт, который никогда не приотовишь.
### Автор:

 - [Рогулин Степан](https://github.com/s-v-rogulin)
 - ребята из яндекса
# Для прекрасного, самого лушего, очаровательного ревьюера, Екатерины(Если тут будет кто-то другой, вы уж извините)
passphrase: NRjeSf

ip: 158.160.75.90


## Примененные технологии:

- [Python 3.9](https://www.python.org/)
- [Django 3.2](https://www.djangoproject.com/)
- [Django Rest Framework 3.14.0](https://www.django-rest-framework.org/)
- [Docker](https://www.docker.com)
- [Nginx](https://nginx.org/ru/)
- [PostgreSQL](https://www.postgresql.org)
- [React](https://react.dev)
- [Gunicorn](https://gunicorn.org)
- [Яндекс.Облако](https://cloud.yandex.ru/) 
- [GitHub Actions](https://docs.github.com/ru/actions)

#### Клонирование проекта

Сперва клонируйте репозиторий и создайте виртуальное окружение(Venv)

```
git clone git@github.com:s-v-rogulin/foodgram-project-react.git
cd foodgram-project-react
python -m venv venv
source venv/Scripts/activate
cd backend
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### Создание .env-файла

```
cd infra
```

```
SECRET_KEY='Секретный ключ Django'
DEBUG=False
ALLOWED_HOSTS= ip_сервера,127.0.0.1,localhost,домен
DB_ENGINE=django.db.backends.postgresql
DB_NAME=foodgram
DB_USER=foodgram_user
DB_PASSWORD=foodgram_password
DB_HOST=db
DB_PORT=5432
```
#### Собираем оркестр
```
docker-compose-local up
```
#### Проводим миграции
```
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```
#### Наполняем базу
```
docker-compose exec backend python manage.py load_to_db
```
#### Статика
```
docker-compose exec backend python manage.py collectstatic --no-input
```
#### Создаем суперпользователя
```
docker-compose exec backend python manage.py createsuperuser
```
