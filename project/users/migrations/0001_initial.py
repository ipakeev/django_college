# Generated by Django 4.0.5 on 2022-06-27 05:09

from django.db import migrations, models
import django.utils.timezone
import project.users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Удалено')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('first_name', models.CharField(max_length=32, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=32, verbose_name='Фамилия')),
                ('patronymic', models.CharField(blank=True, max_length=32, null=True, verbose_name='Отчество')),
                ('degree', models.CharField(blank=True, choices=[('bachelor', 'Бакалавр'), ('master', 'Магистр'), ('candidate', 'Доцент'), ('doctor', 'Профессор')], max_length=16, null=True, verbose_name='Категория')),
                ('group_name', models.CharField(choices=[('Teacher', 'Учитель'), ('Student', 'Студент'), ('OAuth2', 'Через соц.сеть')], max_length=16, verbose_name='Название группы пользователей')),
                ('joined_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Все пользователи',
                'permissions': (('edit_lessons', 'Can create, edit, delete lessons.'), ('view_student_details', "Can view students' marks."), ('send_email', 'Can send email.'), ('view_timetable', 'Can read timetable.')),
            },
            managers=[
                ('objects', project.users.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='OAuth2User',
            fields=[
            ],
            options={
                'verbose_name': 'OAuth2',
                'verbose_name_plural': 'OAuth2',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
            managers=[
                ('objects', project.users.models.UserGroupModelManager()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
            ],
            options={
                'verbose_name': 'Студент',
                'verbose_name_plural': 'Студенты',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
            managers=[
                ('objects', project.users.models.UserGroupModelManager()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
            ],
            options={
                'verbose_name': 'Преподаватель',
                'verbose_name_plural': 'Преподаватели',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
            managers=[
                ('objects', project.users.models.UserGroupModelManager()),
            ],
        ),
    ]
