from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .forms import TransferForm
from module_account.models import Account
from module_card.models import Card
from .services import transfer_by_card

# Create your views here.
class TransferView(View):
    def get(self, request):
        form = TransferForm(user=request.user)
        return render(request, 'module_transfers/transfer.html', {'form': form})

    def post(self, request):
        form = TransferForm(request.POST, user=request.user)
        if form.is_valid():
            from_account = form.cleaned_data['from_account']
            from_card = form.cleaned_data['from_card']
            to_account_number = form.cleaned_data['to_account_number']
            to_card_number = form.cleaned_data['to_card_number']
            amount = form.cleaned_data['amount']

            try:
                if to_account_number:
                    to_account = Account.objects.get(number=to_account_number)
                    if to_account.user == request.user:
                        if from_account.balance < amount:
                            raise ValueError("Недостаточно средств")
                        from_account.balance -= amount
                        to_account.balance += amount
                        from_account.save()
                        to_account.save()
                        messages.success(request, "Перевод между своими счетами выполнен.")
                    else:
                        if from_account.balance < amount:
                            raise ValueError("Недостаточно средств")
                        from_account.balance -= amount
                        to_account.balance += amount
                        from_account.save()
                        to_account.save()
                        messages.success(request, "Перевод другому пользователю выполнен.")
                elif to_card_number:
                    transfer_by_card.transfer_by_card(from_card, to_card_number, amount)
                    messages.success(request, "Перевод на карту выполнен.")
                else:
                    messages.error(request, "Укажите счет или карту получателя.")
                    return render(request, 'module_transfers/transfer.html', {'form': form})

                return redirect('profile')
            except Exception as e:
                messages.error(request, str(e))
        return render(request, 'module_transfers/transfer.html', {'form': form})