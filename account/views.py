from django.http import HttpResponse


def index(request):
    return HttpResponse('Hello World!')
# обработчик запроса, представление (view)