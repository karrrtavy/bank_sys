from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Holding
from .forms import HoldingCreateForm, HoldingDepositForm, HoldingWithdrawForm
from module_transfers.models import TransactionHistory
from module_account.models import Account
from module_card.models import Card

# Create your views here.
@login_required
def holdings_view(request):
    holdings = Holding.objects.filter(user=request.user)
    for holding in holdings:
        holding.calculate_interest()
    
    has_active_holding = holdings.filter(is_active=True).exists()
    
    if request.method == 'POST':
        if 'create_holding' in request.POST:
            form = HoldingCreateForm(request.POST, user=request.user)
            if form.is_valid():
                account = form.cleaned_data['account']
                # проверка, что у пользователя нет активного вклада
                if Holding.objects.filter(user=request.user, is_active=True).exists():
                    messages.error(request, "У вас уже есть активный вклад.")
                else:
                    Holding.objects.create(
                        user=request.user,
                        account=account,
                        is_active=True
                    )
                    messages.success(request, "Вклад успешно создан.")
                return redirect('holdings')
        
        elif 'deposit' in request.POST:
            form = HoldingDepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                holding = get_object_or_404(Holding, user=request.user, is_active=True)
                # поиск основной карты для списания
                main_card = Card.objects.filter(account=holding.account, is_primary=True).first()
                
                if not main_card:
                    messages.error(request, "Не найдена основная карта для списания.")
                    return redirect('holdings')
                
                if main_card.balance < amount:
                    messages.error(request, "Недостаточно средств на карте.")
                    return redirect('holdings')
                
                # списание с карты
                main_card.balance -= amount
                main_card.save()
                
                # зачисление на вклад
                holding.balance += amount
                holding.save()
                
                # запись в историю
                TransactionHistory.objects.create(
                    user=request.user,
                    transaction_type='holding_deposit',
                    description=f'Пополнение вклада на {amount} ₽',
                    amount=amount,
                    card=main_card
                )
                
                messages.success(request, f"Средства успешно зачислены на вклад.")
                return redirect('holdings')
        
        elif 'withdraw' in request.POST:
            form = HoldingWithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                holding = get_object_or_404(Holding, user=request.user, is_active=True)
                
                if holding.balance < amount:
                    messages.error(request, "Недостаточно средств на вкладе.")
                    return redirect('holdings')
                
                # поиск основной карты для зачисления
                main_card = Card.objects.filter(account=holding.account, is_primary=True).first()
                
                if not main_card:
                    messages.error(request, "Не найдена основная карта для зачисления.")
                    return redirect('holdings')
                
                # списание со вклада
                holding.balance -= amount
                holding.save()
                
                # зачисление на карту
                main_card.balance += amount
                main_card.save()
                
                # запись в историю
                TransactionHistory.objects.create(
                    user=request.user,
                    transaction_type='holding_withdraw',
                    description=f'Изъятие с вклада {amount} ₽',
                    amount=amount,
                    card=main_card
                )
                
                messages.success(request, f"Средства успешно изъяты с вклада.")
                return redirect('holdings')
        
        elif 'close' in request.POST:
            holding = get_object_or_404(Holding, user=request.user, is_active=True)
            
            if holding.balance > 0:
                messages.error(request, "Невозможно закрыть вклад с положительным балансом. Сначала изымите средства.")
                return redirect('holdings')
            
            holding.is_active = False
            holding.save()
            
            TransactionHistory.objects.create(
                user=request.user,
                transaction_type='holding_close',
                description='Закрытие вклада'
            )
            
            messages.success(request, "Вклад успешно закрыт.")
            return redirect('holdings')
    
    else:
        deposit_form = HoldingDepositForm()
        withdraw_form = HoldingWithdrawForm()
        create_form = HoldingCreateForm(user=request.user)
    
    context = {
        'holdings': holdings,
        'has_active_holding': has_active_holding,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'create_form': create_form,
    }
    
    return render(request, 'module_holding/holdings.html', context)