Установка
git clone 
cd site-blog/
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
Запуск
python manage.py runserver
Переходим по ссылке
http://127.0.0.1:8000/
База данных
В качестве базы данных используется по умолчанию SQLite

Приложение blog
Приложение blog реализует стандартный функционал Django для блог-сайта: список постов, страница отдельного поста, 
категория, теги и пр.

В качестве базы данных используется SQLite. Поиск по блогу реализован с использованием функционала SQLite.
