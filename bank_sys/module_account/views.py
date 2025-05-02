from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from module_card.models import Card
from .models import Account
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from module_card.models import Card
from .models import Account

class AccountDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        account = get_object_or_404(Account, pk=pk, user=request.user)
        cards = Card.objects.filter(account=account)
        return render(request, 'module_account/account_detail.html', {
            'account': account,
            'cards': cards,
        })
    
class AccountCreateView(LoginRequiredMixin, View):
    def post(self, request):
        Account.objects.create(user=request.user)
        return redirect('profile')
    
class CardCreateView(LoginRequiredMixin, View):
    def post(self, request, account_id):
        account = get_object_or_404(Account, pk=account_id, user=request.user)
        if Card.objects.filter(account=account).count() < 5:
            Card.objects.create(account=account)
        return redirect('account_detail', pk=account.id)