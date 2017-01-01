from django.shortcuts import render, redirect


def index(request):
    return redirect('choice')


def start(request, question_set_id):
    answer_set_id = 228
    first_question_idx = 1
    return redirect('/run/' + str(answer_set_id) + '/' + str(first_question_idx))


def get_choice(request):
    return render(request, 'maps/choice.html', {'sets': [
        {'id': 1, 'title': 'Question Set Sample', 'creator': 'Creator1', 'duration': '40 minutes'}
    ]})


def run(request, answer_set_id, index):
    return render(request, 'maps/task.html', {
        'task': {'title': 'Task1', 'time': 10, 'bounds': [(59.9172, 30.2919), (59.9366, 30.3337)]}
    })


def results(request, answer_set_id):
    return render(request, 'maps/results.html', {})