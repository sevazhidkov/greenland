from django.shortcuts import redirect

from maps import api


def add_map(request):
    api.views.create_map_area(request, form=True)
    return redirect('/control/')


def create_question(request):
    api.views.create_question(request)
    return redirect('/control/')


def create_question_set(request):
    return api.views.create_question_set(request)
