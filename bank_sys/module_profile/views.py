from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from module_account.models import Account
from module_card.models import Card
from module_transfers.models import TransactionHistory

class ProfileView(LoginRequiredMixin, TemplateView):
    """
    @brief Представление профиля пользователя с отображением аккаунтов, карт и основной информации.
    @details Наследует LoginRequiredMixin для ограничения доступа только аутентифицированным пользователям.
             Загружает аккаунты, карты, кредитные карты пользователя и определяет основные аккаунт и карту.
    
    @var template_name Имя шаблона для рендеринга страницы профиля.
    """

    template_name = 'module_profile/dashboard.html'

    def get_context_data(self, **kwargs):
        """
        @brief Формирует контекст для шаблона профиля.
        @details Добавляет в контекст аккаунты пользователя, все карты, кредитные карты,
                 а также основной аккаунт и основную карту, если они существуют.
        
        @param kwargs Дополнительные именованные аргументы.
        
        @var context Словарь данных контекста для шаблона.
        @var user Текущий аутентифицированный пользователь.
        @var accounts QuerySet аккаунтов пользователя.
        @var cards QuerySet карт, связанных с аккаунтами пользователя.
        @var main_account Основной аккаунт пользователя (если есть).
        @var main_card Основная карта, связанная с основным аккаунтом (если есть).
        
        @return dict Контекст для рендеринга шаблона.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user

        accounts = Account.objects.filter(user=user)
        cards = Card.objects.filter(account__in=accounts)

        context['accounts'] = accounts
        context['cards'] = cards
        context['credit_cards'] = user.creditcard_set.all()

        main_account = accounts.filter(is_primary=True).first()
        main_card = None
        if main_account:
            main_card = cards.filter(account=main_account, is_primary=True).first()
        context['main_account'] = main_account
        context['main_card'] = main_card

        return context

class HistoryView(LoginRequiredMixin, ListView):
    """
    @brief Представление истории транзакций пользователя.
    @details Наследует LoginRequiredMixin для ограничения доступа и ListView для отображения списка.
             Отображает последние транзакции пользователя с пагинацией.
    
    @var model Модель, с которой работает представление (TransactionHistory).
    @var template_name Имя шаблона для рендеринга страницы истории.
    @var context_object_name Имя переменной контекста для списка объектов.
    @var paginate_by Количество объектов на странице.
    """

    model = TransactionHistory
    template_name = 'module_profile/history.html'
    context_object_name = 'history'
    paginate_by = 20

    def get_queryset(self):
        """
        @brief Возвращает QuerySet транзакций текущего пользователя, отсортированных по дате.
        
        @return QuerySet Отфильтрованные и отсортированные объекты TransactionHistory.
        """
        return TransactionHistory.objects.filter(user=self.request.user).order_by('-timestamp')
