from django.contrib.auth.backends import ModelBackend
from .models import User

class PhoneBackend(ModelBackend):
    """
    @brief Кастомный бэкенд аутентификации по номеру телефона.
    @details Позволяет аутентифицировать пользователя, используя номер телефона вместо стандартного username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        @brief Пытается аутентифицировать пользователя по номеру телефона и паролю.
        
        @param request Объект HTTP-запроса (может быть None).
        @param username Номер телефона пользователя (используется вместо username).
        @param password Пароль пользователя.
        @param kwargs Дополнительные параметры (игнорируются).
        
        @var user Переменная для хранения найденного пользователя.
        
        @return User|None Объект пользователя при успешной аутентификации, иначе None.
        """
        try:
            user = User.objects.get(phone=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

        return None
