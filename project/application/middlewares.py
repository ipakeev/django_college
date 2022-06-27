from collections.abc import Callable

from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest

from project.application.permissions import GROUP_OAUTH2, GROUP_TEACHER, GROUP_STUDENT
from project.users.models import User


class UserGroupMessageMiddleware:
    tag = "group_message"
    message = {
        GROUP_TEACHER: "Учитель, благодарим за Вашу работу!",
        GROUP_STUDENT: "Студент, готовься к сессии!",
        GROUP_OAUTH2: "Добро пожаловать в наш вуз.",
    }

    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest) -> None:
        response = self.get_response(request)
        self.clear_previous_messages(request)

        user: User = request.user
        if user.is_superuser:
            message = ""
        elif user.is_anonymous:
            message = "Не забудьте авторизоваться."
        else:
            message = self.message[user.group_name]

        if message:
            messages.add_message(request, messages.INFO, message, extra_tags=self.tag)
        return response

    def clear_previous_messages(self, request: WSGIRequest) -> None:
        for msg in messages.get_messages(request):
            if msg.extra_tags != self.tag:
                msg.used = False
