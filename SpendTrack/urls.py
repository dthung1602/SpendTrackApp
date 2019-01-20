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

from spendtrackapp.views import index, account

urlpatterns = [
    path('', index.index_handler, name='index'),
    path('add/', index.add_handler, name='add'),

    path('admin/', admin.site.urls, name='admin'),
    path('account/', include('spendtrackapp.urls.account')),

    path('summarize/', include('spendtrackapp.urls.summarize')),
    path('plan/', include('spendtrackapp.urls.plan')),
    path('settings/', include('spendtrackapp.urls.settings')),
]
