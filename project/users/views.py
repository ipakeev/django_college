from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from project.college.models import Grade
from .forms import EmailMessageForm
from .models import Teacher, Student
from .tasks import send_email
from ..application.settings import config


class TeacherListView(ListView):
    model = Teacher


class TeacherDetailView(DetailView):
    model = Teacher


class StudentListView(ListView):
    model = Student


class StudentDetailView(View):

    def get(self, request: WSGIRequest, pk: int):
        context = {
            "student": Student.objects.filter(id=pk).prefetch_related("courses").first(),
            "grades": Grade.objects.filter(student_id=pk).select_related(
                "timetable",
                "timetable__course",
                "timetable__lesson",
                "timetable__lesson__chair",
            ),
        }
        return render(request, "users/student_detail.html", context=context)


class Contacts(View):

    def get(self, request: WSGIRequest):
        context = {
            "contacts": config.college,
            "form": EmailMessageForm(),
        }
        return render(request, "users/contacts.html", context=context)

    def post(self, request: WSGIRequest):
        form = EmailMessageForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            self.send_to_admin(data["email"], data["message"])
            self.answer_to_user(data["email"])
            messages.add_message(request, messages.SUCCESS, "Сообщение успешно отправлено!")
            form = EmailMessageForm()
        else:
            messages.add_message(request, messages.ERROR, "Произошла ошибка!")

        context = {
            "contacts": config.college,
            "form": form,
        }
        return render(request, "users/contacts.html", context=context)

    def send_to_admin(self, from_email: str, message: str):
        send_email.delay(
            f"[College] Сообщение от {from_email}.",
            message,
            [config.admin.email],
        )

    def answer_to_user(self, from_email: str):
        send_email.delay(
            f"[College] Сообщение получено.",
            "Благодарим за сообщение. Мы ответим в ближайшее время.",
            [from_email],
        )
