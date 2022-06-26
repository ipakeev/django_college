from collections.abc import Callable

from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest

from .groups import GROUP_OAUTH2, GROUP_TEACHER, GROUP_STUDENT
from .models import User


class UserGroupMessageMiddleware:
    message = {
        GROUP_TEACHER: "Благодарим за Вашу работу!",
        GROUP_STUDENT: "Готовься к сессии!",
        GROUP_OAUTH2: "Добро пожаловать в наш вуз.",
    }

    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest) -> None:
        response = self.get_response(request)
        user: User = request.user
        if user.is_superuser:
            return response

        # clear previous middleware's messages
        for msg in messages.get_messages(request):
            if msg.extra_tags != "custom_msg":
                msg.used = False

        if user.is_anonymous:
            message = "Не забудьте авторизоваться."
        else:
            message = self.message[user.get_group_name()]
        if message:
            messages.add_message(request, messages.INFO, message, extra_tags="custom_msg")
        return response
