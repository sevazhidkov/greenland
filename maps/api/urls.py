from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^question_set/', views.list_question_sets),
    url(r'^answer_set/', views.create_answer_set),
]
