from django.http import HttpRequest
from django.shortcuts import render, redirect

from maps.models import *
from maps.api.views import *


def index(request):
    return redirect('choice')


def start(request, question_set_id):
    answer_set = create_answer_set(request.user, question_set_id)
    return redirect('/run/' + str(answer_set.id) + '/' + str(first_question_idx))


def get_choice(request):
    sets = list_question_sets()
    return render(request, 'maps/choice.html', {'sets': sets})


def run(request, answer_set_id, idx):
    return render(request, 'maps/task.html', {
        'task': {'title': 'Task1', 'time': 10, 'bounds': [(59.9172, 30.2919), (59.9366, 30.3337)],
                 'answer_set_id': answer_set_id, 'idx': idx}
    })


def results(request, answer_set_id):
    return render(request, 'maps/results.html', {})
