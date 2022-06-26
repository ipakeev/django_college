from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.views import View


class ErrorView(View):
    status_code: int
    message: str

    def get(self, request: WSGIRequest, exception: Exception):
        response = render(request, "errors.html", context={"message": self.message})
        response.status_code = self.status_code
        return response

    def post(self, request: WSGIRequest, exception):
        return self.get(request, exception)


class BadRequestError(ErrorView):
    status_code = 400
    message = "Неправильный запрос."


class ForbiddenError(ErrorView):
    status_code = 403
    message = "Доступ запрещен."


class NotFoundError(ErrorView):
    status_code = 404
    message = "Не найдено"


class InternalError(ErrorView):
    status_code = 500
    message = "Ошибка сервера. Уже работаем над этим."
