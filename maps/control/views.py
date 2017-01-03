from django.shortcuts import render
from maps.api.views import *


def control(request):
    return render(request, 'maps/control/index.html', {'sets': list_question_sets()})


def create_map(request):
    if request.method == 'GET':
        return render(request, 'maps/control/add.html')
