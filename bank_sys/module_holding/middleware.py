from django.utils.deprecation import MiddlewareMixin
from .models import Holding, CreditCard

class HoldingInterestMiddleware(MiddlewareMixin):
    """
    @brief Middleware для автоматического начисления процентов на активные холдинги и кредитные карты пользователя.
    @details При каждом запросе аутентифицированного пользователя вычисляет и применяет проценты к его активным холдингам и кредитным картам.
    """

    def process_request(self, request):
        """
        @brief Обрабатывает входящий HTTP-запрос.
        @details Если пользователь аутентифицирован, получает все активные холдинги и кредитные карты пользователя,
                 и вызывает метод calculate_interest() для каждого из них.
        
        @param request Объект HTTP-запроса.
        
        @var holdings QuerySet активных холдингов пользователя.
        @var holding Экземпляр модели Holding из QuerySet.
        @var credit_cards QuerySet активных кредитных карт пользователя.
        @var card Экземпляр модели CreditCard из QuerySet.
        
        @return None
        """
        if request.user.is_authenticated:
            holdings = Holding.objects.filter(user=request.user, is_active=True)
            for holding in holdings:
                holding.calculate_interest()
            
            credit_cards = CreditCard.objects.filter(user=request.user, is_active=True)
            for card in credit_cards:
                card.calculate_interest()
