## Как запустить локально
1. Для запуска локально необходимо перейти в директорию vetbot2 и создать и активировать виртуальное окружение:

`python3 -m venv .venv` 

`source venv/bin/activate`

2. Установите зависимости

```
pip3 install --upgrade pip
pip3 install -r app/requirements.txt
```

3. Создайте файл `.env` и заполните его по аналогии с `.env.example`

4. Сделайте миграции и примените их:

`python3 manage.py makemigrations`

`python3 manage.py migrate`

5. Создайте суперюзера:

`python3 manage.py createsuperuser`

6. Запустите Джанго:

`python3 manage.py runserver`

7. Запустите бота(прописать в другом окне терминала):

`python3 manage.py start_bot`

