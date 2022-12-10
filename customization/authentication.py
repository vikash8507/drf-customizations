from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import get_user_model
from rest_framework import exceptions

User = get_user_model()

class CustomAuthClass(BaseAuthentication):
    
    def authenticate(self, request):
        username = request.META.get('HTTP_X_USERNAME')
        if not username:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)