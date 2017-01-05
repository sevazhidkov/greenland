from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^question_set_list/', views.question_set_list),
    url(r'^answer_set/', views.create_answer_set),
    url(r'^answer/', views.create_answer),
    url(r'^question/', views.question),
    url(r'^contour_tile/(?P<question_id>\d+)', views.contour_tile),
    url(r'^map_area/', views.create_map_area),
    url(r'^question_set/', views.create_question_set),
]
