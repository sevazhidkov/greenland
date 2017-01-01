"""greenland URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import maps.views

urlpatterns = [
    url(r'^$', maps.views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^start/(?P<question_set_id>\d+)/', maps.views.start, name='start'),
    url(r'^choice/', maps.views.get_choice, name='choice'),
    url(r'^run/(?P<answer_set_id>\d+)/(?P<index>\d+)', maps.views.run, name='task'),
    url(r'^results/(?P<answer_set_id>\d+)', maps.views.results, name='results')
]