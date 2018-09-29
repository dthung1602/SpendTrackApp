from django.http.response import HttpResponse


def year(request, year):
    return HttpResponse('year')


def month(request, year, month):
    return HttpResponse('month')


def week(request, year, week):
    return HttpResponse('week')


def date_range(request, start_date, end_date):
    return HttpResponse('date')
