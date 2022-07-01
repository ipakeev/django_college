from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, Http404
from django.views import View
from django.views.generic import ListView, DetailView
from social_django.utils import load_strategy

from project.application.permissions import SendEmailPermission, ViewStudentDetailsPermission, GROUP_OAUTH2
from project.application.settings import config
from project.college.models import Grade
from utils.jwt import obtain_tokens_for_user, refresh_tokens, get_tokens
from .forms import EmailMessageForm, LoginForm
from .models import Teacher, Student, User
from .tasks import send_email


class TeacherListView(ListView):
    model = Teacher


class TeacherDetailView(DetailView):
    model = Teacher


class StudentListView(ListView):
    model = Student


class StudentDetailView(PermissionRequiredMixin, View):
    permission_required = ViewStudentDetailsPermission.title

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


class ContactsView(PermissionRequiredMixin, View):
    permission_required = SendEmailPermission.title

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


class LoginJWTView(View):

    def get(self, request: WSGIRequest):
        user = authenticate(wsgi_request=request)
        if user is None or user.is_deleted:
            messages.add_message(request, messages.ERROR, f"Пользователь не найден.")
        elif not user.is_active:
            messages.add_message(request, messages.ERROR, f"Пользователь не активен.")
        else:
            login(request, user)
            return render(request, "root.html")

        return LoginView().get(request)


class LoginView(View):

    def get(self, request: WSGIRequest):
        context = {
            "form": LoginForm(),
        }
        return render(request, "users/login.html", context=context)

    def post(self, request: WSGIRequest):
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            email = data["email"]
            user = authenticate(username=email, password=data["password"])
            if user is None or user.is_deleted:
                messages.add_message(request, messages.ERROR, f"Пользователь {email} не найден.")
            elif not user.is_active:
                messages.add_message(request, messages.ERROR, f"Пользователь {email} не активен.")
            else:
                login(request, user)
                return render(request, "root.html")

        context = {
            "form": LoginForm(),
        }
        return render(request, "users/login.html", context=context)


class LogoutView(LoginRequiredMixin, View):

    def get(self, request: WSGIRequest):
        logout(request)
        return render(request, "root.html")


class AccountView(LoginRequiredMixin, View):

    def get(self, request: WSGIRequest, tokens=None):
        user: User = request.user
        context = {
            "group": user.group_name or "Администратор",
        }
        if user.group_name == GROUP_OAUTH2:
            context["oauth2_token"] = user.social_auth.get(provider='google-oauth2').access_token
        else:
            context.update(get_tokens(request))

        if tokens:
            request.COOKIES.update(tokens)

        return render(request, "users/account.html", context=context)

    def post(self, request: WSGIRequest):
        user: User = request.user
        if "oauth2_refresh_token" in request.POST:
            social = request.user.social_auth.get(provider='google-oauth2')
            social.refresh_token(load_strategy())
            tokens = None
        elif "jwt_obtain_token" in request.POST:
            tokens = obtain_tokens_for_user(user)
        elif "jwt_refresh_token" in request.POST:
            tokens = refresh_tokens(request)
        elif "jwt_delete_token" in request.POST:
            tokens = {"delete_tokens": "true"}
        else:
            raise Http404
        return self.get(request, tokens=tokens)
