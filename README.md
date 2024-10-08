# Этот проект - дипломная работа студентов группы Py53-onl.

# Ссылка на сайт:
https://diplom-t24j.onrender.com/

# Описание:
Сайт социальной сети с профилями, группами, новостями, комментами и внутренней почтой и групповым чатом на websocket.

# Технологии:

1. Языки программирования: Python v3.10, JavaScript
2. Дополнительно: HTML5, CSS3
3. Framework: Django, ReactJS
4. Database: SQLLite

# Размещение:
Сайт размещен на бесплатном хостинге Render.

# Разработчики:
1. https://github.com/ViktoriaKonoplyanik
2. https://github.com/fedyaslonn
3. https://github.com/Danya2kk
4. https://github.com/sajicklevo
5. https://github.com/Saatarko

# Для локальной загрузки требуется:
1. Загрузить сайт на ПК.
2. Установить виртуальное окружение с Python v3.10
3. Установить библиотеки. (в проекте использовался poetry)
   Для этого Вам нужно установить poetry - pip install poetry
   Затем для устновки всех библиотек  -   poetry install
4. Для запуска в wsgi можно запустить проект через manage.py  (python manage.py runserver)
   для запуска в asgi запускаемся через runserver.py  python runserver.py 
  ( при запуске проекта в локальном виде  на адресе "0.0.0.0:8000"  нужно для входа использовать адрес "localhost:8000")

   Дополнительно. Команда длля запуска сайта на сервере или через Docker 
   
# Команда для запуска приложения
CMD ["poetry", "run", "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "socnet.asgi:application", "--bind", "0.0.0.0:8000"]

# This project is a diploma work of students of the Py53-onl group.

# Link to the site:
https://diplom-t24j.onrender.com/

# Description:
A social network site with profiles, groups, news, comments and internal mail and group chat on websocket.

# Technologies:

1. Programming languages: Python v3.10, JavaScript
2. Additional: HTML5, CSS3
3. Framework: Django, ReactJS
4. Database: SQLLite

# Deploy:
The site is hosted on the free Render hosting.

# Developers:
1. https://github.com/ViktoriaKonoplyanik
2. https://github.com/fedyaslonn
3. https://github.com/Danya2kk
4. https://github.com/sajicklevo

# For local download you need:
1. Download the site to your PC.
2. Install a virtual environment with Python v3.10
3. Install libraries. (poetry was used in the project)
To do this, you needs to install poetry - pip install poetry
Then to install all libraries - poetry install
4. To run in wsgi, you can run the project via manage.py (python manage.py runserver)
To run in asgi, run via runserver.py python runserver.py
(when running the project locally at the address "0.0.0.0:8000", you need to use the address "localhost:8000" to log in)

Additionally. Command to run the site on the server or via Docker

# Command to run the application
CMD ["poetry", "run", "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "socnet.asgi:application", "--bind", "0.0.0.0:8000"]



