from django.shortcuts import redirect

from maps import api


def add_map(request):
    return api.views.create_map_area(request, form=True)


def create_question(request):
    return api.views.create_question(request)


def create_question_set(request):
    return api.views.create_question_set(request)
