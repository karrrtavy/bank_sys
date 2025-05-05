from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from module_card.models import Card
from .models import Account
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime, timedelta
from module_transfers.models import TransactionHistory
from django.db import models

class AccountDetailView(LoginRequiredMixin, View):
    """
    @brief Отображает детальную информацию по счёту пользователя.
    
    @details Получает аккаунт по pk и текущему пользователю, а также связанные с ним карты.
    Отображает шаблон с данными аккаунта и карт.
    """
    def get(self, request, pk):
        """
        @brief Обрабатывает GET-запрос.
        
        @param request Объект HTTP-запроса.
        @param pk Первичный ключ аккаунта.
        
        @return HttpResponse Рендер шаблона с данными аккаунта и карт.
        """
        account = get_object_or_404(Account, pk=pk, user=request.user)
        cards = Card.objects.filter(account=account)
        return render(request, 'module_account/account_detail.html', {
            'account': account,
            'cards': cards,
        })

class AccountCreateView(LoginRequiredMixin, View):
    """
    @brief Создаёт новый счёт пользователя.
    
    @details Проверяет, что у пользователя не более 5 счетов. Если лимит превышен - отображает ошибку.
    Иначе создаёт новый счёт и отображает сообщение об успехе.
    """
    def post(self, request, *args, **kwargs):
        """
        @brief Обрабатывает POST-запрос создания нового счёта.
        
        @param request Объект HTTP-запроса.
        @param args Дополнительные позиционные аргументы.
        @param kwargs Дополнительные именованные аргументы.
        
        @return HttpResponse Перенаправление на профиль пользователя.
        """
        user_accounts_count = Account.objects.filter(user=request.user).count()
        if user_accounts_count >= 5:
            messages.error(request, "Вы не можете создать больше 5 счетов.")
            return redirect('profile')
        Account.objects.create(user=request.user)
        messages.success(request, "Новый счет успешно создан.")
        return redirect('profile')

class CardCreateView(LoginRequiredMixin, View):
    """
    @brief Создаёт новую карту для указанного счёта.
    
    @details Проверяет, что у счёта не более 5 карт. Если лимит не превышен - создаёт карту.
    """
    def post(self, request, account_id):
        """
        @brief Обрабатывает POST-запрос создания карты.
        
        @param request Объект HTTP-запроса.
        @param account_id Идентификатор счёта, к которому привязывается карта.
        
        @return HttpResponse Перенаправление на страницу детализации счёта.
        """
        account = get_object_or_404(Account, pk=account_id, user=request.user)
        if Card.objects.filter(account=account).count() < 5:
            Card.objects.create(account=account)
        return redirect('account_detail', pk=account.id)

class AccountDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    @brief Удаляет счёт пользователя.
    
    @details Использует стандартный DeleteView с проверкой, что счёт принадлежит текущему пользователю.
    """
    model = Account
    template_name = 'module_account/account_confirm_delete.html'
    success_url = reverse_lazy('profile')

    def test_func(self):
        """
        @brief Проверяет, что пользователь имеет право удалять данный счёт.
        
        @return bool True, если счёт принадлежит текущему пользователю, иначе False.
        """
        account = self.get_object()
        return account.user == self.request.user

class CardDeleteView(LoginRequiredMixin, View):
    """
    @brief Удаляет карту пользователя с проверками.
    
    @details Запрещает удаление последней карты и основной карты.
    При удалении переносит баланс удаляемой карты на основную карту.
    """
    def post(self, request, card_id):
        """
        @brief Обрабатывает POST-запрос удаления карты.
        
        @param request Объект HTTP-запроса.
        @param card_id Идентификатор удаляемой карты.
        
        @return HttpResponse Перенаправление на страницу детализации счёта с сообщением.
        """
        card = get_object_or_404(Card, id=card_id, account__user=request.user)
        cards_qs = Card.objects.filter(account=card.account)
        
        if cards_qs.count() <= 1:
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
    """
    @brief Делает выбранную карту основной для счёта.
    """
    def post(self, request, card_id):
        """
        @brief Обрабатывает POST-запрос установки основной карты.
        
        @param request Объект HTTP-запроса.
        @param card_id Идентификатор карты.
        
        @return HttpResponse Перенаправление на страницу детализации счёта с сообщением.
        """
        card = get_object_or_404(Card, id=card_id, account__user=request.user)
        account = card.account

        Card.objects.filter(account=account, is_primary=True).update(is_primary=False)
        card.is_primary = True
        card.save()

        messages.success(request, "Карта сделана основной.")
        return redirect('account_detail', pk=account.id)

class AccountMakePrimaryView(LoginRequiredMixin, View):
    """
    @brief Делает выбранный счёт основным для пользователя.
    """
    def post(self, request, pk):
        """
        @brief Обрабатывает POST-запрос установки основного счёта.
        
        @param request Объект HTTP-запроса.
        @param pk Первичный ключ счёта.
        
        @return HttpResponse Перенаправление на профиль пользователя с сообщением.
        """
        account = get_object_or_404(Account, pk=pk, user=request.user)
        Account.objects.filter(user=request.user, is_primary=True).update(is_primary=False)
        account.is_primary = True
        account.save()
        messages.success(request, f"Счет №{account.number} теперь основной.")
        return redirect('profile')

class AccountStatementView(LoginRequiredMixin, View):
    """
    @brief Генерирует PDF-выписку по счёту за последние 30 дней.
    
    @details Использует библиотеку ReportLab для создания PDF с таблицей транзакций.
    """
    def get(self, request, pk):
        """
        @brief Обрабатывает GET-запрос для генерации выписки.
        
        @param request Объект HTTP-запроса.
        @param pk Первичный ключ счёта.
        
        @return HttpResponse PDF-файл с выпиской.
        """
        account = get_object_or_404(Account, pk=pk, user=request.user)
        
        buffer = BytesIO()
        
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        
        import os
        import reportlab
        from django.conf import settings

        reportlab.rl_config.TTFSearchPath.append(os.path.join(settings.BASE_DIR, 'static', 'fonts'))

        pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))
        
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        p.setFont("DejaVuSans-Bold", 16)
        p.drawString(1 * inch, height - 1 * inch, f"Выписка по счету №{account.number}")
        
        p.setFont("DejaVuSans", 12)
        p.drawString(1 * inch, height - 1.5 * inch, f"Клиент: {request.user.get_full_name()}")
        p.drawString(1 * inch, height - 1.8 * inch, f"Дата формирования: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        p.drawString(1 * inch, height - 2.1 * inch, f"Текущий баланс: {account.cards_total_balance:.2f} ₽")
        
        thirty_days_ago = datetime.now() - timedelta(days=30)
        transactions = TransactionHistory.objects.filter(
            models.Q(source_account=account) | models.Q(target_account=account),
            timestamp__gte=thirty_days_ago
        ).order_by('-timestamp')
        
        data = [["Дата", "Тип операции", "Сумма", "Описание"]]
        
        for t in transactions:
            amount = ""
            if t.amount:
                if t.transaction_type == 'transfer_in':
                    amount = f"+{t.amount:.2f} ₽"
                else:
                    amount = f"-{t.amount:.2f} ₽"
            
            data.append([
                t.timestamp.strftime("%d.%m.%Y %H:%M"),
                t.get_transaction_type_display(),
                amount,
                t.description[:50] + "..." if len(t.description) > 50 else t.description
            ])
        
        table = Table(data, colWidths=[1.5*inch, 1.5*inch, 1*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'DejaVuSans'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        table.wrapOn(p, width, height)
        table.drawOn(p, 1 * inch, height - 3 * inch - len(data)*0.2*inch)
        
        p.setFont("DejaVuSans", 10)
        p.drawString(1 * inch, 0.5 * inch, "Подпись ответственного лица: ___________________")
        
        p.showPage()
        p.save()
        
        pdf = buffer.getvalue()
        buffer.close()
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="account_statement_{account.number}.pdf"'
        response.write(pdf)
        
        return response