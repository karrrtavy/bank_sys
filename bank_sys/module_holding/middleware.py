from django.utils.deprecation import MiddlewareMixin
from .models import Holding, CreditCard

class HoldingInterestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            # начисление процентов по вкладам
            holdings = Holding.objects.filter(user=request.user, is_active=True)
            for holding in holdings:
                holding.calculate_interest()
            
            # начисление процентов по кредитным картам
            credit_cards = CreditCard.objects.filter(user=request.user, is_active=True)
            for card in credit_cards:
                card.calculate_interest()