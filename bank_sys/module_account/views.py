from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from module_card.models import Card
from .models import Account
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

# Create your views here.
class AccountDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        account = get_object_or_404(Account, pk=pk, user=request.user)
        cards = Card.objects.filter(account=account)
        return render(request, 'module_account/account_detail.html', {
            'account': account,
            'cards': cards,
        })
    
class AccountCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user_accounts_count = Account.objects.filter(user=request.user).count()
        if user_accounts_count >= 5:
            messages.error(request, "Вы не можете создать больше 5 счетов.")
            return redirect('profile')
        Account.objects.create(user=request.user)
        messages.success(request, "Новый счет успешно создан.")
        return redirect('profile')
    
class CardCreateView(LoginRequiredMixin, View):
    def post(self, request, account_id):
        account = get_object_or_404(Account, pk=account_id, user=request.user)
        if Card.objects.filter(account=account).count() < 5:
            Card.objects.create(account=account)
        return redirect('account_detail', pk=account.id)
    
class AccountDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Account
    template_name = 'module_account/account_confirm_delete.html'
    success_url = reverse_lazy('profile')

    def test_func(self):
        account = self.get_object()
        return account.user == self.request.user