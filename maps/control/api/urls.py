from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^upload/', views.add_map),
    url(r'^create_question/', views.create_question),
    url(r'^create_question_set/', views.create_question_set)
]
