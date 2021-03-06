"""SpendTrack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from spendtrackapp.views import index

urlpatterns = [
    path('', index.index_handler, name='index'),
    path('about/', index.about_handler, name='about'),
    path('legalnotice/', index.legal_notice_handler, name='legalnotice'),
    path('home/', index.home_handler, name='home'),

    path('entry/', include('spendtrackapp.urls.entry')),
    path('account/', include('spendtrackapp.urls.account')),
    path('summarize/', include('spendtrackapp.urls.summarize')),
    path('plan/', include('spendtrackapp.urls.plan')),

    path('admin/', admin.site.urls, name='admin'),
]
