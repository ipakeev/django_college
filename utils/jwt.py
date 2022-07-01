from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from project.users.models import User


def get_tokens(request: WSGIRequest) -> dict[str, str]:
    return {
        'access': request.COOKIES.get("access"),
        'refresh': request.COOKIES.get("refresh"),
    }


def obtain_tokens_for_user(user: User) -> dict[str, str]:
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }


def refresh_tokens(request: WSGIRequest) -> dict[str, str]:
    return TokenRefreshSerializer().validate(get_tokens(request))


def set_tokens(response: HttpResponse, jwt_tokens: dict) -> None:
    for key, value in jwt_tokens.items():
        response.set_cookie(key, value)


def delete_tokens(response: HttpResponse):
    response.delete_cookie("access")
    response.delete_cookie("refresh")
    response.delete_cookie("delete_tokens")
