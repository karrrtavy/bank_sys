from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Holding, CreditCard
from .forms import (
    HoldingCreateForm, HoldingDepositForm, HoldingWithdrawForm,
    CreditCardCreateForm, CreditCardPayForm, CreditCardWithdrawForm
)
from module_account.models import Account
from module_transfers.models import TransactionHistory
from decimal import Decimal

@login_required
def holdings_view(request):
    """
    @brief Представление для управления вкладами и кредитными картами пользователя.
    @details Позволяет создавать, пополнять, снимать и закрывать вклады, а также управлять кредитными картами.
    Обрабатывает различные POST-запросы, связанные с этими действиями, и отображает соответствующие формы и списки.

    @param request Объект HTTP-запроса Django.

    @var holdings QuerySet вкладов пользователя.
    @var has_active_holding Логический флаг наличия активного вклада.
    @var credit_cards QuerySet кредитных карт пользователя.
    @var has_active_credit_card Логический флаг наличия активной кредитной карты.
    @var create_form Форма создания вклада.
    @var deposit_form Форма пополнения вклада.
    @var withdraw_form Форма изъятия с вклада.
    @var credit_card_form Форма создания кредитной карты.
    @var pay_credit_form Форма погашения кредита.
    @var holding_id Идентификатор вклада, с которым производится операция.
    @var holding Экземпляр модели Holding, с которым производится операция.
    @var amount Сумма операции (пополнение, снятие, погашение и т.д.).
    @var main_card Основная карта, связанная с аккаунтом вклада или кредитной карты.
    @var card_id Идентификатор кредитной карты.
    @var card Экземпляр модели CreditCard, с которым производится операция.
    @var credit_limit Кредитный лимит, рассчитываемый для новой кредитной карты.

    @return HttpResponse Рендерит страницу с формами и списками или перенаправляет после обработки POST-запроса.
    """
    holdings = Holding.objects.filter(user=request.user)
    has_active_holding = holdings.filter(is_active=True).exists()
    credit_cards = CreditCard.objects.filter(user=request.user)
    has_active_credit_card = credit_cards.filter(is_active=True).exists()
    
    if request.method == 'POST':
        if 'create_holding' in request.POST:
            create_form = HoldingCreateForm(request.POST, user=request.user)
            if create_form.is_valid():
                account = create_form.cleaned_data['account']
                Holding.objects.create(user=request.user, account=account)
                messages.success(request, "Вклад успешно создан")
                return redirect('holdings')
        
        elif 'deposit' in request.POST:
            deposit_form = HoldingDepositForm(request.POST)
            if deposit_form.is_valid():
                holding_id = request.POST.get('holding_id')
                holding = Holding.objects.get(id=holding_id, user=request.user)
                amount = deposit_form.cleaned_data['amount']
                
                if holding.account.cards_total_balance >= amount:
                    holding.balance += amount
                    holding.save()
                    
                    main_card = holding.account.card_set.filter(is_primary=True).first()
                    if main_card:
                        main_card.balance -= amount
                        main_card.save()
                    TransactionHistory.objects.create(
                        user=request.user,
                        transaction_type='holding_deposit',
                        description=f'Пополнение вклада №{holding.id}',
                        amount=amount,
                        source_account=holding.account,
                        card=main_card
                    )
                    messages.success(request, f"Вклад пополнен на {amount} ₽")
                else:
                    messages.error(request, "Недостаточно средств на счете")
                return redirect('holdings')
        
        elif 'withdraw' in request.POST:
            withdraw_form = HoldingWithdrawForm(request.POST)
            if withdraw_form.is_valid():
                holding_id = request.POST.get('holding_id')
                holding = Holding.objects.get(id=holding_id, user=request.user)
                amount = withdraw_form.cleaned_data['amount']
                if holding.balance >= amount:
                    holding.balance -= amount
                    holding.save()
                    
                    main_card = holding.account.card_set.filter(is_primary=True).first()
                    if main_card:
                        main_card.balance += amount
                        main_card.save()
                    
                    TransactionHistory.objects.create(
                        user=request.user,
                        transaction_type='holding_withdraw',
                        description=f'Изъятие с вклада №{holding.id}',
                        amount=amount,
                        target_account=holding.account,
                        card=main_card
                    )
                    messages.success(request, f"Средства в размере {amount} ₽ сняты с вклада")
                else:
                    messages.error(request, "Недостаточно средств на вкладе")
                return redirect('holdings')
        
        elif 'close' in request.POST:
            holding_id = request.POST.get('holding_id')
            holding = Holding.objects.get(id=holding_id, user=request.user)
            if holding.balance > 0:
                main_card = holding.account.card_set.filter(is_primary=True).first()
                if main_card:
                    main_card.balance += holding.balance
                    main_card.save()
                    TransactionHistory.objects.create(
                        user=request.user,
                        transaction_type='holding_withdraw',
                        description=f'Закрытие вклада №{holding.id}',
                        amount=holding.balance,
                        target_account=holding.account,
                        card=main_card
                    )
            holding.is_active = False
            holding.save()
            TransactionHistory.objects.create(
                user=request.user,
                transaction_type='holding_close',
                description=f'Закрытие вклада №{holding.id}',
                source_account=holding.account
            )
            messages.success(request, "Вклад успешно закрыт")
            return redirect('holdings')
        
        elif 'create_credit_card' in request.POST:
            create_form = CreditCardCreateForm(request.POST, user=request.user)
            if create_form.is_valid():
                account = create_form.cleaned_data['account']
                credit_limit = request.user.income * Decimal('0.5')
                if not CreditCard.objects.filter(user=request.user, is_active=True).exists():
                    credit_card = CreditCard.objects.create(
                        user=request.user,
                        account=account,
                        credit_limit=credit_limit
                    )
                    messages.success(request, "Кредитная карта успешно создана")
                else:
                    messages.error(request, "У вас уже есть активная кредитная карта")
                return redirect('holdings')
        
        elif 'pay_credit' in request.POST:
            pay_form = CreditCardPayForm(request.POST)
            if pay_form.is_valid():
                card_id = request.POST.get('card_id')
                card = CreditCard.objects.get(id=card_id, user=request.user)
                amount = pay_form.cleaned_data['amount']
                main_card = card.account.card_set.filter(is_primary=True).first()
                if main_card and main_card.balance >= amount:
                    main_card.balance -= amount
                    main_card.save()
                    card.balance += amount
                    card.save()
                    TransactionHistory.objects.create(
                        user=request.user,
                        transaction_type='credit_payment',
                        description=f'Погашение кредита по карте ****{card.number[-4:]}',
                        amount=amount,
                        source_account=card.account,
                        card=main_card
                    )
                    messages.success(request, f"Кредит погашен на {amount} ₽")
                    if card.balance >= 0:
                        card.is_active = False
                        card.save()
                        messages.success(request, "Кредит полностью погашен, карта закрыта")
                else:
                    messages.error(request, "Недостаточно средств для погашения")
                return redirect('holdings')
        
        elif 'close_credit' in request.POST:
            card_id = request.POST.get('card_id')
            card = CreditCard.objects.get(id=card_id, user=request.user)
            if card.balance >= 0:
                card.is_active = False
                card.save()
                messages.success(request, "Кредитная карта закрыта")
            else:
                messages.error(request, "Невозможно закрыть карту с непогашенным кредитом")
            return redirect('holdings')
    
    else:
        create_form = HoldingCreateForm(user=request.user)
        deposit_form = HoldingDepositForm()
        withdraw_form = HoldingWithdrawForm()
        credit_card_form = CreditCardCreateForm(user=request.user)
        pay_credit_form = CreditCardPayForm()
    
    return render(request, 'module_holding/holdings.html', {
        'holdings': holdings,
        'has_active_holding': has_active_holding,
        'create_form': create_form,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'credit_cards': credit_cards,
        'has_active_credit_card': has_active_credit_card,
        'credit_card_form': credit_card_form,
        'pay_credit_form': pay_credit_form,
    })


@login_required
def credit_withdraw_view(request):
    """
    @brief Представление для снятия средств с кредитной карты.
    @details Обрабатывает форму снятия средств с кредитной карты, вызывает метод withdraw у CreditCard.
    В случае успеха или ошибки выводит соответствующее сообщение и перенаправляет пользователя.

    @param request Объект HTTP-запроса Django.

    @var form Форма снятия средств с кредитной карты.
    @var card Экземпляр CreditCard, с которой производится снятие.
    @var amount Сумма снятия.

    @return HttpResponse Рендерит страницу с формой или перенаправляет после обработки POST-запроса.
    """
    if request.method == 'POST':
        form = CreditCardWithdrawForm(request.POST, user=request.user)
        if form.is_valid():
            card = form.cleaned_data['card']
            amount = form.cleaned_data['amount']
            try:
                card.withdraw(amount)
                messages.success(request, f"Средства {amount} ₽ успешно сняты с кредитной карты")
            except ValueError as e:
                messages.error(request, str(e))
            return redirect('holdings')
    else:
        form = CreditCardWithdrawForm(user=request.user)
    
    return render(request, 'module_holding/credit_withdraw.html', {'form': form})
