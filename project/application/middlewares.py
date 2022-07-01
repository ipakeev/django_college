from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

from project.application.permissions import GROUP_OAUTH2, GROUP_TEACHER, GROUP_STUDENT
from project.users.models import User
from utils.jwt import get_tokens, set_tokens, delete_tokens


class UserGroupMessageMiddleware(MiddlewareMixin):
    tag = "group_message"
    message = {
        GROUP_TEACHER: "Учитель, благодарим за Вашу работу!",
        GROUP_STUDENT: "Студент, готовься к сессии!",
        GROUP_OAUTH2: "Добро пожаловать в наш вуз.",
    }

    def process_response(self, request: WSGIRequest, response) -> None:
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


class JWTTokenMiddleware(MiddlewareMixin):

    def process_response(self, request: WSGIRequest, response: HttpResponse) -> HttpResponse:
        if request.COOKIES.get("delete_tokens"):
            delete_tokens(response)
            return response

        tokens = get_tokens(request)
        if tokens["access"]:
            set_tokens(response, tokens)
        return response
