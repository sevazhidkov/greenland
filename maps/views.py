from django.shortcuts import render, redirect


def index(request):
    return redirect('choice')


def get_choice(request):
    return render(request, 'maps/choice.html', {'sets': [
        {'id': 1, 'title': 'Question Set Sample', 'creator': 'Creator1', 'duration': '40 minutes'}
    ]})


def get_task(request):
    return render(request, 'maps/task.html', {
        'task': {'title': 'Task1', 'time': 10, 'bounds': [(59.9172, 30.2919), (59.9366, 30.3337)]}
    })
