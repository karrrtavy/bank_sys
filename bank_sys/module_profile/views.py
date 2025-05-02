from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from module_account.models import Account
from module_card.models import Card

class ProfileView (LoginRequiredMixin, TemplateView):
    template_name = 'module_profile/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        main_account = Account.objects.filter(user=user, is_primary=True).first()
        main_card = None
        if main_account:
            main_card = Card.objects.filter(account=main_account, is_primary=True).first()
        context['main_account'] = main_account
        context['main_card'] = main_card
        context['accounts'] = Account.objects.filter(user=user)
        return context