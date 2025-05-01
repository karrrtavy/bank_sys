from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from module_account.models import Account
from module_card.models import Card

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'module_profile/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accounts'] = Account.objects.filter(user=self.request.user)
        context['cards'] = Card.objects.filter(account__user=self.request.user)
        return context