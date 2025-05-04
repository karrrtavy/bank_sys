from django.utils.deprecation import MiddlewareMixin
from .models import Holding

class HoldingInterestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            # начисление процентов по всем активным вкладам пользователей
            holdings = Holding.objects.filter(user=request.user, is_active=True)
            for holding in holdings:
                holding.calculate_interest()