Для запуска локально необходимо перейти в директорию vetbot2 и создать и активировать виртуальное окружение:

`python3 -m venv .venv` 
`source venv/bin/activate`
`pip install -r requirements.txt`
Создайте файл .env и заполните его
Сделайте миграции и примените их:
`python3 manage.py makemigrations`
`python3 manage.py migrate`
Для создания суперюзера:
`python3 manage.py createsuperuser`
Для запуска джанго:
`python3 manage.py runserver`
Для запуска бота(прописать в другом окне терминала):
`python3 manage.py start_bot`

