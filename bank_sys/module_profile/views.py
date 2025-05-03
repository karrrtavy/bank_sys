from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from module_account.models import Account
from module_card.models import Card
from django.views.generic import ListView
from module_transfers.models import TransactionHistory

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'module_profile/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        accounts = Account.objects.filter(user=user)
        cards = Card.objects.filter(account__in=accounts)

        context['accounts'] = accounts
        context['cards'] = cards

        main_account = accounts.filter(is_primary=True).first()
        main_card = None
        if main_account:
            main_card = cards.filter(account=main_account, is_primary=True).first()
        context['main_account'] = main_account
        context['main_card'] = main_card

        return context
    
class HistoryView(LoginRequiredMixin, ListView):
    model = TransactionHistory
    template_name = 'module_profile/history.html'
    context_object_name = 'history'
    paginate_by = 20

    def get_queryset(self):
        return TransactionHistory.objects.filter(user=self.request.user).order_by('-timestamp')