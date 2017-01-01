import json
import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from maps.models import QuestionSet, AnswerSet


def list_question_sets(request):
    objects = QuestionSet.objects.all()
    items = []
    for obj in objects:
        items.append({
            'title': obj.title,
            'max_duration': obj.max_duration.seconds,
            'creator': {
                'full_name': obj.creator.get_full_name()
            }
        })
    return HttpResponse(json.dumps(items))


@csrf_exempt
def create_answer_set(request):
    obj = AnswerSet()
    obj.student = request.user
    obj.question_set = QuestionSet.objects.get(id=request.POST['question_set_id'])
    obj.start_time = datetime.datetime.utcnow()
    obj.save()
    return HttpResponse(json.dumps({
        'answer_set_id': obj.id,
        'start_index': 0,
        'max_duration': obj.question_set.max_duration.seconds
    }))
