from django.shortcuts import render

def index(request):
    """
    @brief Отображает главную страницу сайта.
    @details Обрабатывает HTTP-запрос и возвращает отрендеренный шаблон 'index.html'.
    
    @param request Объект HTTP-запроса.
    
    @return HttpResponse Ответ с отрендеренным шаблоном главной страницы.
    """
    return render(request, 'index.html')