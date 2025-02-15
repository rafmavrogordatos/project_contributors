from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.backends import BaseBackend
from .models import User

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_data = request.data
        username = raw_data.get("username")
        password = raw_data.get("password")

        if not username or not password:
            return None  # Let the default JWT behavior handle this

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed("No active account found with the given credentials")

        if not user.check_password(password):  # Use your custom check_password method
            raise AuthenticationFailed("No active account found with the given credentials")

        refresh = RefreshToken.for_user(user)
        update_last_login(None, user)  # Update last login timestamp

        return (user, refresh.access_token)
