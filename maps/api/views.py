import json
from django.http import HttpResponse
from maps.models import QuestionSet


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
