from django.http import HttpRequest
from django.shortcuts import render, redirect

from maps.models import *
from maps.api.views import *


def index(request):
    return redirect('choice')


def start(request, question_set_id):
    answer_set = create_answer_set(request.user, question_set_id)
    return redirect('/run/' + str(answer_set.id) + '/0')


def get_choice(request):
    sets = list_question_sets()
    return render(request, 'maps/choice.html', {'sets': sets})


def run(request, answer_set_id, idx):
    answer_set = AnswerSet.objects.get(pk=answer_set_id)
    question = answer_set.question_set.get_questions()[int(idx)]
    area = question.map_area.display_area
    return render(request, 'maps/task.html', {
        'task': {'title': 'Task #' + str(int(idx) + 1), 'time': question.max_duration.seconds, 'bounds': [(area.west, area.north), (area.east, area.south)],
                 'answer_set_id': answer_set_id, 'idx': idx}
    })


def results(request, answer_set_id):
    return render(request, 'maps/results.html', {})
