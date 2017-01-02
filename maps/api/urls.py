import getpass
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^question_set/', views.http_list_question_sets),
    url(r'^answer_set/', views.http_create_answer_set),
    url(r'^answer/', views.create_answer),
    url(r'^question/', views.get_question),
]
