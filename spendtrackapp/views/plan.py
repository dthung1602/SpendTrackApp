from django.http.response import HttpResponse


def index(request):
    return HttpResponse('index')


def add(request):
    return HttpResponse('add')


def delete(request):
    return HttpResponse('del')


def edit(request):
    return HttpResponse('edit')
