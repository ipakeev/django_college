from django.contrib.auth.backends import BaseBackend
from django.core.handlers.wsgi import WSGIRequest
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

from project.users.models import User
from utils.jwt import get_tokens, refresh_tokens


class JWTTokenAuthBackend(BaseBackend):

    def authenticate(self, _, **kwargs) -> User | None:
        request: WSGIRequest = kwargs.get("wsgi_request")
        if not request:
            return

        token = get_tokens(request)["access"]
        if token:
            try:
                validated_token = AccessToken(token=token, verify=True)
            except TokenError:
                refreshed_tokens = refresh_tokens(request)
                request.COOKIES.update(refreshed_tokens)
                validated_token = AccessToken(token=refreshed_tokens["access"], verify=True)

            user = JWTTokenUserAuthentication().get_user(validated_token)
            return self.get_user(user.id)

    def get_user(self, user_id) -> User | None:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
