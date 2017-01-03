import getpass
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^upload/', views.add_map),
]
