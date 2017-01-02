import json
import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from maps.models import QuestionSet, AnswerSet


def list_question_sets():
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

    return list(map(lambda q:
                    {'id': q.id, 'title': q.title, 'creator': q.creator.get_full_name(),
                     'duration': pretty_duration(q.max_duration.seconds)},
                    QuestionSet.objects.all()))


def http_list_question_sets(request):
    return HttpResponse(json.dumps(list_question_sets()))


def create_answer_set(user, question_set_id):
    obj = AnswerSet()
    obj.student = user
    obj.question_set = QuestionSet.objects.get(id=question_set_id)
    obj.start_time = datetime.datetime.utcnow()
    obj.save()
    return obj


@csrf_exempt
def http_create_answer_set(request):
    obj = create_answer_set(request.user, request.POST['question_set_id'])
    return HttpResponse(json.dumps({
        'answer_set_id': obj.id,
        'start_index': 0,
        'max_duration': obj.question_set.max_duration.seconds
    }))
