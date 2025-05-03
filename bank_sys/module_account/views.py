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
    
class CardDeleteView(LoginRequiredMixin, View):
    def post(self, request, card_id):
        card = get_object_or_404(Card, id=card_id, account__user=request.user)
        cards_qs = Card.objects.filter(account=card.account)
        
        if Card.objects.filter(account=card.account).count() <= 1:
            messages.error(request, "Нельзя удалить последнюю карту")
            return redirect('account_detail', pk=card.account.id)
            
        if card.is_primary:
            messages.error(request, "Нельзя удалить основную карту")
            return redirect('account_detail', pk=card.account.id)
        
        main_card = cards_qs.filter(is_primary=True).first()
        if main_card and main_card != card:
            main_card.balance += card.balance
            main_card.save()
            
        card.delete()
        messages.success(request, "Карта успешно удалена")
        return redirect('account_detail', pk=card.account.id)
    
class CardMakePrimaryView(LoginRequiredMixin, View):
    def post(self, request, card_id):
        card = get_object_or_404(Card, id=card_id, account__user=request.user)
        account = card.account

        Card.objects.filter(account=account, is_primary=True).update(is_primary=False)
        card.is_primary = True
        card.save()

        messages.success(request, "Карта сделана основной.")
        return redirect('account_detail', pk=account.id)
    
class AccountMakePrimaryView(LoginRequiredMixin, View):
    def post(self, request, pk):
        account = get_object_or_404(Account, pk=pk, user=request.user)
        Account.objects.filter(user=request.user, is_primary=True).update(is_primary=False)
        account.is_primary = True
        account.save()
        messages.success(request, f"Счет №{account.number} теперь основной.")
        return redirect('profile')