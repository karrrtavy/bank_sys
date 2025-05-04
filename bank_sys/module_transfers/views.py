from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from module_account.models import Account
from module_card.models import Card
from .forms import TransferForm
from .models import TransactionHistory
from module_holding.models import CreditCard

@login_required
def transfer_view(request):
    if request.method == 'POST':
        form = TransferForm(request.POST, user=request.user)
        if form.is_valid():
            transfer_from = form.cleaned_data['transfer_from']
            transfer_to = form.cleaned_data['transfer_to']
            amount = form.cleaned_data['amount']
            receiver_number = form.cleaned_data['receiver_number']

            # 1. определение источника списания
            if transfer_from == 'account':
                sender_account = form.cleaned_data['sender_account']
                # поиск основной карты отправителя
                sender_card = Card.objects.filter(account=sender_account, is_primary=True).first()
                if not sender_card:
                    messages.error(request, "У вашего счета нет основной карты для списания.")
                    return redirect('transfer')
                sender_label = f"Счет №{sender_account.number} (основная карта ****{sender_card.number[-4:]})"
                sender_balance = sender_card.balance
                sender_user = sender_account.user
            else:
                sender_card = form.cleaned_data['sender_card']
                sender_label = f"Карта ****{sender_card.number[-4:]}"
                sender_balance = sender_card.balance
                sender_user = sender_card.account.user

            # проверка принадлежности
            if sender_user != request.user:
                messages.error(request, "Вы не можете переводить с чужого счета/карты.")
                return redirect('transfer')

            # определение получателя
            if transfer_to == 'account':
                receiver_account = Account.objects.filter(number=receiver_number).first()
                if not receiver_account:
                    messages.error(request, "Счет получателя не найден.")
                    return redirect('transfer')
                # поиск основной карты счета-получателя
                receiver_card = Card.objects.filter(account=receiver_account, is_primary=True).first()
                if not receiver_card:
                    messages.error(request, "У счета-получателя нет основной карты.")
                    return redirect('transfer')
                receiver_label = f"Счет №{receiver_account.number} (основная карта ****{receiver_card.number[-4:]})"
                receiver_user = receiver_account.user
            else:
                receiver_card = Card.objects.filter(number=receiver_number).first()
                if not receiver_card:
                    messages.error(request, "Карта получателя не найдена.")
                    return redirect('transfer')
                receiver_label = f"Карта ****{receiver_card.number[-4:]}"
                receiver_user = receiver_card.account.user

            # проверка баланса
            if sender_balance < amount:
                messages.error(request, "Недостаточно средств.")
                return redirect('transfer')

            # списание
            sender_card.balance -= amount
            sender_card.save()

            # зачисление
            receiver_card.balance += amount
            receiver_card.save()

            # история переводов
            TransactionHistory.objects.create(
                user=sender_user,
                transaction_type='transfer_out',
                description=f'Перевод на {receiver_label}',
                source_account=sender_account if transfer_from == 'account' else None,
                card=sender_card if transfer_from == 'card' or transfer_from == 'account' else None,
                target_account=receiver_account if transfer_to == 'account' else None,
                amount=amount
            )
            TransactionHistory.objects.create(
                user=receiver_user,
                transaction_type='transfer_in',
                description=f'Зачисление с {sender_label}',
                source_account=sender_account if transfer_from == 'account' else None,
                card=sender_card if transfer_from == 'card' or transfer_from == 'account' else None,
                target_account=receiver_account if transfer_to == 'account' else None,
                amount=amount
            )

            has_negative_credit = CreditCard.objects.filter(
            user=request.user, 
            is_active=True, 
            balance__lt=0
            ).exists()
    
            if has_negative_credit:
                messages.error(request, "У вас есть непогашенный кредит. Переводы запрещены.")
                return redirect('profile')

            messages.success(request, f"Перевод {amount} ₽ на {receiver_label} выполнен успешно.")
            return redirect('profile')
    else:
        form = TransferForm(user=request.user)
    return render(request, 'module_transfers/transfers.html', {'form': form})
