from django.contrib.auth.backends import ModelBackend
from .models import User

class PhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Пробуем найти пользователя по телефону
            user = User.objects.get(phone=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            # Если не нашли по телефону, пробуем стандартный способ
            return None
        
        return None