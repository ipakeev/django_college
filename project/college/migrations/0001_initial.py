# Generated by Django 4.0.5 on 2022-06-27 05:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auditorium',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Удалено')),
                ('address', models.CharField(max_length=64, verbose_name='Адрес')),
            ],
            options={
                'verbose_name': 'Аудитория',
                'verbose_name_plural': 'Аудитории',
            },
        ),
        migrations.CreateModel(
            name='Chair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Удалено')),
                ('title', models.CharField(max_length=64, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Кафедра',
                'verbose_name_plural': 'Кафедры',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Удалено')),
                ('title', models.CharField(max_length=64, verbose_name='Название курса')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Удалено')),
                ('value', models.PositiveSmallIntegerField(verbose_name='Оценка')),
            ],
            options={
                'verbose_name': 'Оценка за урок',
                'verbose_name_plural': 'Оценки за уроки',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Удалено')),
                ('theme', models.CharField(max_length=64, verbose_name='Тема занятия')),
                ('homework', models.TextField(blank=True, null=True, verbose_name='Домашнее задание')),
            ],
            options={
                'verbose_name': 'Занятие',
                'verbose_name_plural': 'Занятия',
            },
        ),
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Удалено')),
                ('date', models.DateField(verbose_name='Дата расписания')),
                ('start_at', models.TimeField(verbose_name='Время начала занятия')),
                ('duration', models.PositiveSmallIntegerField(default=90, verbose_name='Продолжительность (мин.)')),
                ('auditorium', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='timetable', to='college.auditorium', verbose_name='Аудитория')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='timetable', to='college.course', verbose_name='Курс')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='timetable', to='college.lesson', verbose_name='Занятие')),
            ],
            options={
                'verbose_name': 'Расписание',
                'verbose_name_plural': 'Расписание',
                'ordering': ('date', 'start_at'),
            },
        ),
    ]
