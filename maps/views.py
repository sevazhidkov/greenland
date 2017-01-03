from django.shortcuts import render, redirect
from maps.actions import questions
from maps.models import AnswerSet


def index(request):
    return redirect('choice')


def start(request, question_set_id):
    answer_set = questions.create_answer_set(request.user, question_set_id)
    return redirect('/run/' + str(answer_set.id) + '/0')


def get_choice(request):
    sets = questions.question_set_list()
    return render(request, 'maps/choice.html', {'sets': sets})


def run(request, answer_set_id, idx):
    answer_set = AnswerSet.objects.get(pk=answer_set_id)
    idx = int(idx)
    questions = answer_set.question_set.get_questions()
    if idx >= len(questions):
        return redirect('/results/' + str(answer_set_id))
    question = questions[idx]
    area = question.map_area.display_area
    contour_area = question.map_area.contour_map_reference
    return render(request, 'maps/task.html', {
        'task': {'title': 'Task #' + str(idx + 1), 'time': question.max_duration.seconds,
                 'bounds': [(area.west, area.north), (area.east, area.south)],
                 'contour_bounds': [(contour_area.west, contour_area.north), (contour_area.east, contour_area.south)],
                 'answer_set_id': answer_set_id, 'idx': idx, 'question_id': question.id}
    })


def results(request, answer_set_id):
    return render(request, 'maps/results.html', {})
