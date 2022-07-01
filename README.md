# Учебный проект на Django

### **Общие сведения:**
- Python 3.10
- Django 4.0
- Django REST framework 3.13
- SQLite3
- Celery 5.2
- Redis 4.3

### **Цель:** 
Описать учебный процесс в неком вузе.

### **Авторизация:** 
- OAuth2
- стандартная
- JWT-токен (выпускается после стандартной авторизации)

### **Доступ к страницам зависит от группы пользователя:** 
- Аноним
- OAuth2
- Преподаватель
- Студент

### **DRF:** 
- /api/lesson/
- /api/grade/
- /api/token/

### **Запуск проекта:**
- `pip install -r requirements.txt`
- `etc/local/config.yml` - создать конфигурационный файл
- `python manage.py migrate`
- `python manage.py createsuperuser`
- `python manage.py create_groups` - создать группы с пермишенами
- `python manage.py fill_db` - заполнить БД фейковыми данными
- `python manage.py runserver`
- Celery:
  - Unix: `celery -A project worker -c 1 -l INFO`
  - Windows: `celery -A project worker -c 1 -l INFO -P gevent`