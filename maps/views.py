from django.shortcuts import render


def get_task(request):
    return render(request, 'maps/task.html', {'tasks': [
        {'title': 'Task', 'bounds': [(59.9172, 30.2919), (59.9366, 30.3337)]}
    ]})
