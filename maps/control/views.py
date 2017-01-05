from django.shortcuts import render
from maps.api.views import *
from maps.actions.questions import *


def control(request):
    return render(request, 'maps/control/index.html', {'sets': question_set_list(), 'questions': question_list()})


def create_map(request):
    if request.method == 'GET':
        return render(request, 'maps/control/add_map.html')


def http_create_question(request):
    return render(request, 'maps/control/add_question.html', {'map_areas': map_area_list()})
