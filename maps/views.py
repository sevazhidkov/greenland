from django.shortcuts import render, redirect

from maps.models import *
from maps.api.views import *


def index(request):
    return redirect('choice')


def start(request, question_set_id):
    answer_set_id = 228
    first_question_idx = 1
    return redirect('/run/' + str(answer_set_id) + '/' + str(first_question_idx))


def get_choice(request):
    def pretty_duration(seconds):
        hr = seconds // 3600
        res = ''
        if hr > 0:
            res += str(hr) + ' hours '
        seconds -= hr * 3600
        mn = seconds // 60
        if mn > 0:
            res += str(mn) + ' minutes '
        seconds -= mn * 60
        if seconds > 0:
            res += str(seconds) + ' seconds '
        return res.rstrip()

    sets = list(map(lambda q:
                    {'id': q.id, 'title': q.title, 'creator': q.creator, 'duration': pretty_duration(q.max_duration.seconds)},
                    QuestionSet.objects.all()))
    print(sets)
    return render(request, 'maps/choice.html', {'sets': sets})


def run(request, answer_set_id, idx):
    return render(request, 'maps/task.html', {
        'task': {'title': 'Task1', 'time': 10, 'bounds': [(59.9172, 30.2919), (59.9366, 30.3337)],
                 'answer_set_id': answer_set_id, 'idx': idx}
    })


def results(request, answer_set_id):
    return render(request, 'maps/results.html', {})
