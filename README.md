# Учебный проект на Django

### **Общие сведения:**
- Python 3.10
- Django 4.0
- SQLite3

### **Цель:** 
Описать учебный процесс в неком вузе.

### **Запуск проекта:**
- `pip install -r requirements.txt`
- `cd project`
- `python manage.py migrate`
- `python manage.py createsuperuser`
- `python manage.py fill_db` - заполнить БД фейковыми данными
- `python manage.py runserver`
- Celery:
  - Unix: `celery -A project worker -c 1 -l INFO`
  - Windows: `celery -A project worker -c 1 -l INFO -P gevent`