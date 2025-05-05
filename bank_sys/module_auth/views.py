from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_backends
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegistrationForm, CustomLoginForm

# Create your views here.

class Registration(CreateView):
    """
    @brief Класс представления для регистрации нового пользователя.
    @details Использует форму RegistrationForm, сохраняет пользователя с хешированным паролем,
             автоматически логинит пользователя после успешной регистрации и перенаправляет на профиль.
    
    @var form_class Класс формы регистрации (RegistrationForm).
    @var template_name Шаблон для отображения страницы регистрации.
    @var success_url URL для перенаправления после успешной регистрации.
    """

    form_class = RegistrationForm
    template_name = 'module_auth/sign_up.html'
    success_url = reverse_lazy('profile')
    
    def form_valid(self, form):
        """
        @brief Обрабатывает валидную форму регистрации.
        @details Создаёт пользователя, устанавливает пароль, задаёт username (если не указан),
                 сохраняет пользователя, выполняет автоматический вход и перенаправляет на success_url.
        
        @param form Объект формы с валидированными данными.
        
        @var user Экземпляр модели User, созданный из формы.
        @var backend Строка с полным путем к бэкенду аутентификации.
        
        @return HttpResponseRedirect Перенаправление на страницу профиля.
        """
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        if not user.username:
            user.username = user.phone
        user.save()
        self.object = user
        backend = get_backends()[0]
        login(self.request, user, backend=backend.__module__ + '.' + backend.__class__.__name__)
        return redirect(self.get_success_url())
    
    def dispatch(self, request, *args, **kwargs):
        """
        @brief Обрабатывает входящий HTTP-запрос.
        @details Если пользователь уже аутентифицирован, перенаправляет на профиль,
                 иначе вызывает стандартный метод dispatch родительского класса.
        
        @param request Объект HTTP-запроса.
        @param args Дополнительные позиционные аргументы.
        @param kwargs Дополнительные именованные аргументы.
        
        @return HttpResponseRedirect или HttpResponse Возвращает либо редирект, либо результат родительского dispatch.
        """
        if request.user.is_authenticated:
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)


class Login(LoginView):
    """
    @brief Класс представления для входа пользователя.
    @details Использует кастомную форму CustomLoginForm, шаблон для страницы входа,
             автоматически перенаправляет аутентифицированных пользователей.
    
    @var form_class Класс формы для аутентификации (CustomLoginForm).
    @var template_name Шаблон для отображения страницы входа.
    @var redirect_authenticated_user Флаг, указывающий на автоматический редирект аутентифицированных пользователей.
    """
    form_class = CustomLoginForm
    template_name = 'module_auth/sign_in.html'
    redirect_authenticated_user = True
