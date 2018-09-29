from django.http.response import HttpResponse


def index(request):
    return HttpResponse('index')


def edit(request):
    return HttpResponse('edit')
