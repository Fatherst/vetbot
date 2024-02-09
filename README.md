# Телеграм бот для клиентов вет клиники
## Как запустить локально
1. Создайте и активируйте виртуальное окружение:
```
python3 -m venv .venv
. .venv/bin/activate
```
2. Установите зависимости
```
pip3 install --upgrade pip
pip3 install -r app/requirements.txt
```
3. Создайте файл `.env` и заполните его по аналогии с `.env.template`
4. Поднимите postgres:
```
docker run -d \
  -p 5432:5432 \
  -v pg_data:/var/lib/postgresql/data_vet_bot \
  -e POSTGRES_PASSWORD=divan \
  -e POSTGRES_USER=divan \
  -e POSTGRES_DB=divan \
  postgres:13 
```

5. Примените миграции:
```
python3 app/manage.py migrate
```
6. Создайте супер пользователя:
```
python3 app/manage.py createsuperuser
```
7. Запустите джанго:
```
python3 app/manage.py runserver 8000
```
8. Запустите бота (прописать в другом окне терминала):
```
python3 app/manage.py start_bot
```

9. Запустите celery и celery beat:
```
celery -A bot_admin worker --beat --scheduler django --loglevel=info --detach
```

## Как запустить локально через docker
```
docker-compose -f docker-compose.dev.yml up -d --build
```
