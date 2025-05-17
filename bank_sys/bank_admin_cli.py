import os
import sys
import django
from django.core.exceptions import ObjectDoesNotExist
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from datetime import datetime

# Настройка Django окружения
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank_sys.settings')
django.setup()

from module_auth.models import User
from module_account.models import Account
from module_card.models import Card
from module_transfers.models import TransactionHistory

console = Console()

def display_welcome():
    console.print("[bold blue]BankAdmin Console[/bold blue]")
    console.print("Административная консоль банковской системы\n")

def display_menu():
    menu = """
1. Управление клиентами
2. Управление счетами
3. Управление картами
4. История операций
5. Генерация отчетов
0. Выход
"""
    console.print(menu)

def manage_clients():
    while True:
        console.print("\n[bold]Управление клиентами[/bold]")
        console.print("1. Список клиентов")
        console.print("2. Поиск клиента")
        console.print("3. Добавить клиента")
        console.print("4. Блокировка/разблокировка")
        console.print("0. Назад")
        
        choice = Prompt.ask("Выберите действие", choices=["1", "2", "3", "4", "0"])
        
        if choice == "1":
            clients = User.objects.all().order_by('-date_joined')
            table = Table(title="Список клиентов")
            table.add_column("ID", style="cyan")
            table.add_column("Телефон")
            table.add_column("ФИО")
            table.add_column("Дата регистрации")
            table.add_column("Активен", style="green")
            
            for client in clients:
                table.add_row(
                    str(client.id),
                    client.phone,
                    client.get_full_name() or "-",
                    client.date_joined.strftime("%d.%m.%Y %H:%M"),
                    "Да" if client.is_active else "Нет"
                )
            console.print(table)
            
        elif choice == "2":
            phone = Prompt.ask("Введите номер телефона клиента (+7XXXXXXXXXX)")
            try:
                client = User.objects.get(phone=phone)
                display_client_details(client)
            except ObjectDoesNotExist:
                console.print("[red]Клиент не найден[/red]")
                
        elif choice == "3":
            console.print("\n[bold]Добавление нового клиента[/bold]")
            phone = Prompt.ask("Телефон (+7XXXXXXXXXX)")
            name = Prompt.ask("Имя", default="")
            surname = Prompt.ask("Фамилия", default="")
            income = Prompt.ask("Доход", default="0")
            
            try:
                client = User.objects.create(
                    phone=phone,
                    username=phone,
                    name=name,
                    surname=surname,
                    income=income
                )
                client.set_password(phone[-4:])  # Пароль - последние 4 цифры телефона
                client.save()
                console.print(f"[green]Клиент {phone} успешно создан![/green]")
                console.print(f"[yellow]Временный пароль: {phone[-4:]}[/yellow]")
            except Exception as e:
                console.print(f"[red]Ошибка: {e}[/red]")
                
        elif choice == "4":
            phone = Prompt.ask("Введите номер телефона клиента (+7XXXXXXXXXX)")
            try:
                client = User.objects.get(phone=phone)
                action = "разблокировать" if not client.is_active else "заблокировать"
                if Confirm.ask(f"Вы уверены, что хотите {action} клиента {phone}?"):
                    client.is_active = not client.is_active
                    client.save()
                    console.print(f"[green]Клиент {phone} успешно {'разблокирован' if client.is_active else 'заблокирован'}[/green]")
            except ObjectDoesNotExist:
                console.print("[red]Клиент не найден[/red]")
                
        elif choice == "0":
            break

def display_client_details(client):
    table = Table(title=f"Информация о клиенте {client.phone}", show_header=False)
    table.add_row("ID", str(client.id))
    table.add_row("Телефон", client.phone)
    table.add_row("ФИО", client.get_full_name() or "-")
    table.add_row("Доход", f"{client.income} ₽")
    table.add_row("Дата регистрации", client.date_joined.strftime("%d.%m.%Y %H:%M"))
    table.add_row("Активен", "Да" if client.is_active else "Нет", style="green" if client.is_active else "red")
    console.print(table)
    
    # Счета клиента
    accounts = Account.objects.filter(user=client)
    if accounts.exists():
        console.print("\n[bold]Счета клиента:[/bold]")
        acc_table = Table()
        acc_table.add_column("Номер счета")
        acc_table.add_column("Баланс")
        acc_table.add_column("Основной")
        acc_table.add_column("Дата создания")
        
        for acc in accounts:
            acc_table.add_row(
                acc.number,
                f"{acc.balance} ₽",
                "Да" if acc.is_primary else "Нет",
                acc.created_at.strftime("%d.%m.%Y %H:%M")
            )
        console.print(acc_table)

def manage_accounts():
    while True:
        console.print("\n[bold]Управление счетами[/bold]")
        console.print("1. Список счетов по клиенту")
        console.print("2. Создать счет")
        console.print("3. Закрыть счет")
        console.print("0. Назад")
        
        choice = Prompt.ask("Выберите действие", choices=["1", "2", "3", "0"])
        
        if choice == "1":
            phone = Prompt.ask("Введите номер телефона клиента (+7XXXXXXXXXX)")
            try:
                client = User.objects.get(phone=phone)
                accounts = Account.objects.filter(user=client)
                
                if not accounts.exists():
                    console.print("[yellow]У клиента нет счетов[/yellow]")
                    continue
                    
                display_client_accounts(client, accounts)
                
            except ObjectDoesNotExist:
                console.print("[red]Клиент не найден[/red]")
                
        elif choice == "2":
            phone = Prompt.ask("Введите номер телефона клиента (+7XXXXXXXXXX)")
            try:
                client = User.objects.get(phone=phone)
                if Confirm.ask(f"Создать новый счет для клиента {client.phone}?"):
                    account = Account.objects.create(user=client)
                    console.print(f"[green]Счет №{account.number} успешно создан![/green]")
            except ObjectDoesNotExist:
                console.print("[red]Клиент не найден[/red]")
                
        elif choice == "3":
            account_number = Prompt.ask("Введите номер счета для закрытия")
            try:
                account = Account.objects.get(number=account_number)
                if Confirm.ask(f"Закрыть счет №{account.number} клиента {account.user.phone}?"):
                    if account.card_set.exists():
                        console.print("[red]Нельзя закрыть счет с привязанными картами[/red]")
                    else:
                        account.delete()
                        console.print("[green]Счет успешно закрыт[/green]")
            except ObjectDoesNotExist:
                console.print("[red]Счет не найден[/red]")
                
        elif choice == "0":
            break

def display_client_accounts(client, accounts):
    console.print(f"\n[bold]Счета клиента {client.phone}:[/bold]")
    table = Table()
    table.add_column("Номер счета")
    table.add_column("Баланс")
    table.add_column("Основной")
    table.add_column("Дата создания")
    table.add_column("Карт")
    
    for acc in accounts:
        table.add_row(
            acc.number,
            f"{acc.balance} ₽",
            "Да" if acc.is_primary else "Нет",
            acc.created_at.strftime("%d.%m.%Y %H:%M"),
            str(acc.card_set.count())
        )
    console.print(table)

def manage_cards():
    while True:
        console.print("\n[bold]Управление картами[/bold]")
        console.print("1. Выпустить новую карту")
        console.print("2. Блокировка карты")
        console.print("3. Просмотр карт клиента")
        console.print("0. Назад")
        
        choice = Prompt.ask("Выберите действие", choices=["1", "2", "3", "0"])
        
        if choice == "1":
            account_number = Prompt.ask("Введите номер счета для выпуска карты")
            try:
                account = Account.objects.get(number=account_number)
                if account.card_set.count() >= 5:
                    console.print("[red]На счету уже максимальное количество карт (5)[/red]")
                    continue
                    
                if Confirm.ask(f"Выпустить новую карту для счета №{account.number}?"):
                    card = Card.objects.create(account=account)
                    console.print(f"[green]Карта ****{card.number[-4:]} успешно выпущена![/green]")
            except ObjectDoesNotExist:
                console.print("[red]Счет не найден[/red]")
                
        elif choice == "2":
            card_number = Prompt.ask("Введите номер карты для блокировки (16 цифр)")
            try:
                card = Card.objects.get(number=card_number)
                if Confirm.ask(f"Заблокировать карту ****{card.number[-4:]} клиента {card.account.user.phone}?"):
                    card.delete()
                    console.print("[green]Карта успешно заблокирована[/green]")
            except ObjectDoesNotExist:
                console.print("[red]Карта не найдена[/red]")
                
        elif choice == "3":
            phone = Prompt.ask("Введите номер телефона клиента (+7XXXXXXXXXX)")
            try:
                client = User.objects.get(phone=phone)
                cards = Card.objects.filter(account__user=client)
                
                if not cards.exists():
                    console.print("[yellow]У клиента нет карт[/yellow]")
                    continue
                    
                display_client_cards(client, cards)
                
            except ObjectDoesNotExist:
                console.print("[red]Клиент не найден[/red]")
                
        elif choice == "0":
            break

def display_client_cards(client, cards):
    console.print(f"\n[bold]Карты клиента {client.phone}:[/bold]")
    table = Table()
    table.add_column("Номер карты")
    table.add_column("Счет")
    table.add_column("Баланс")
    table.add_column("Основная")
    table.add_column("Дата выпуска")
    
    for card in cards:
        table.add_row(
            f"****{card.number[-4:]}",
            card.account.number,
            f"{card.balance} ₽",
            "Да" if card.is_primary else "Нет",
            card.created_at.strftime("%d.%m.%Y %H:%M")
        )
    console.print(table)

def view_transactions():
    while True:
        console.print("\n[bold]История операций[/bold]")
        console.print("1. По клиенту")
        console.print("2. По счету")
        console.print("3. По карте")
        console.print("0. Назад")
        
        choice = Prompt.ask("Выберите действие", choices=["1", "2", "3", "0"])
        
        if choice == "1":
            phone = Prompt.ask("Введите номер телефона клиента (+7XXXXXXXXXX)")
            try:
                client = User.objects.get(phone=phone)
                transactions = TransactionHistory.objects.filter(user=client).order_by('-timestamp')[:50]
                
                if not transactions.exists():
                    console.print("[yellow]Нет операций по данному клиенту[/yellow]")
                    continue
                    
                display_transactions(transactions, f"Последние операции клиента {client.phone}")
                
            except ObjectDoesNotExist:
                console.print("[red]Клиент не найден[/red]")
                
        elif choice == "2":
            account_number = Prompt.ask("Введите номер счета")
            try:
                account = Account.objects.get(number=account_number)
                transactions = TransactionHistory.objects.filter(
                    models.Q(source_account=account) | 
                    models.Q(target_account=account)
                ).order_by('-timestamp')[:50]
                
                if not transactions.exists():
                    console.print("[yellow]Нет операций по данному счету[/yellow]")
                    continue
                    
                display_transactions(transactions, f"Операции по счету №{account.number}")
                
            except ObjectDoesNotExist:
                console.print("[red]Счет не найден[/red]")
                
        elif choice == "3":
            card_number = Prompt.ask("Введите номер карты (16 цифр)")
            try:
                card = Card.objects.get(number=card_number)
                transactions = TransactionHistory.objects.filter(card=card).order_by('-timestamp')[:50]
                
                if not transactions.exists():
                    console.print("[yellow]Нет операций по данной карте[/yellow]")
                    continue
                    
                display_transactions(transactions, f"Операции по карте ****{card.number[-4:]}")
                
            except ObjectDoesNotExist:
                console.print("[red]Карта не найдена[/red]")
                
        elif choice == "0":
            break

def display_transactions(transactions, title):
    table = Table(title=title)
    table.add_column("Дата")
    table.add_column("Тип")
    table.add_column("Сумма")
    table.add_column("Описание")
    
    for t in transactions:
        amount = f"{t.amount} ₽" if t.amount else "-"
        color = "green" if t.transaction_type in ['transfer_in', 'holding_withdraw', 'credit_payment'] else "red"
        table.add_row(
            t.timestamp.strftime("%d.%m.%Y %H:%M"),
            t.get_transaction_type_display(),
            f"[{color}]{amount}[/{color}]",
            t.description
        )
    console.print(table)

def generate_reports():
    console.print("\n[bold]Генерация отчетов[/bold]")
    console.print("1. Отчет по клиентам")
    console.print("2. Отчет по счетам")
    console.print("3. Отчет по операциям")
    console.print("0. Назад")
    
    choice = Prompt.ask("Выберите отчет", choices=["1", "2", "3", "0"])
    
    if choice == "1":
        filename = f"clients_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("ID;Телефон;ФИО;Доход;Дата регистрации;Активен;Кол-во счетов\n")
            for client in User.objects.all():
                f.write(
                    f"{client.id};{client.phone};{client.get_full_name() or '-'};"
                    f"{client.income};{client.date_joined.strftime('%d.%m.%Y %H:%M')};"
                    f"{'Да' if client.is_active else 'Нет'};{client.account_set.count()}\n"
                )
        console.print(f"[green]Отчет сохранен в файл {filename}[/green]")
        
    elif choice == "2":
        filename = f"accounts_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Номер счета;Клиент;Баланс;Основной;Дата создания;Кол-во карт\n")
            for acc in Account.objects.all():
                f.write(
                    f"{acc.number};{acc.user.phone};{acc.balance};"
                    f"{'Да' if acc.is_primary else 'Нет'};"
                    f"{acc.created_at.strftime('%d.%m.%Y %H:%M')};{acc.card_set.count()}\n"
                )
        console.print(f"[green]Отчет сохранен в файл {filename}[/green]")
        
    elif choice == "3":
        start_date = Prompt.ask("Начальная дата (ДД.ММ.ГГГГ)", default="01.01.2023")
        end_date = Prompt.ask("Конечная дата (ДД.ММ.ГГГГ)", default=datetime.now().strftime("%d.%m.%Y"))
        
        try:
            start = datetime.strptime(start_date, "%d.%m.%Y")
            end = datetime.strptime(end_date, "%d.%m.%Y")
            
            filename = f"transactions_report_{start_date}_{end_date}.csv".replace(".", "")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("Дата;Тип операции;Клиент;Сумма;Описание\n")
                for t in TransactionHistory.objects.filter(
                    timestamp__date__range=(start.date(), end.date())
                ):
                    f.write(
                        f"{t.timestamp.strftime('%d.%m.%Y %H:%M')};"
                        f"{t.get_transaction_type_display()};"
                        f"{t.user.phone};"
                        f"{t.amount if t.amount else '-'};"
                        f"{t.description}\n"
                    )
            console.print(f"[green]Отчет сохранен в файл {filename}[/green]")
        except ValueError:
            console.print("[red]Неверный формат даты[/red]")

def main():
    display_welcome()
    
    while True:
        display_menu()
        choice = Prompt.ask("Выберите раздел", choices=["1", "2", "3", "4", "5", "0"])
        
        if choice == "1":
            manage_clients()
        elif choice == "2":
            manage_accounts()
        elif choice == "3":
            manage_cards()
        elif choice == "4":
            view_transactions()
        elif choice == "5":
            generate_reports()
        elif choice == "0":
            console.print("[blue]До свидания![/blue]")
            break

if __name__ == "__main__":
    main()