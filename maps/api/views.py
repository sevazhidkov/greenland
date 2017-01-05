import json
import datetime
import imghdr
from django.http import JsonResponse, HttpResponse

from maps.actions import questions
from maps.models import QuestionSet, AnswerSet, Answer, Question, LatLngBounds, MapArea


def question_set_list(request):
    return JsonResponse(questions.question_set_list())


def create_answer_set(request):
    obj = questions.create_answer_set(request.user, request.POST['question_set_id'])
    return JsonResponse({
        'answer_set_id': obj.id,
        'start_index': 0,
        'max_duration': obj.question_set.max_duration.seconds
    })


def create_answer(request):
    now = datetime.datetime.utcnow()
    data = json.loads(request.body.decode('utf-8'))
    answer_set = AnswerSet.objects.get(id=data['answer_set_id'])
    question_set = answer_set.question_set
    if question_set.max_duration.seconds < now.timestamp() - answer_set.start_time.timestamp():
        return JsonResponse({
            'status_message': 'Test is already over',
        }, status=403)
    question_index = int(data['index'])
    answer = Answer()
    answer.answer_set = answer_set
    answer.question_set = question_set
    answer.question = Question.objects.get(id=json.loads(question_set.question_ids)[question_index])
    if 'answer' in data:
        answer.answer_data = json.dumps(data['answer'])
        assert answer.question.actions.validate_answer_data(answer.answer_data)
    else:
        answer.answer_data = json.dumps(None)
    scoring_data = answer.question.actions.get_scoring_data(json.loads(answer.question.reference_data),
                                                            json.loads(answer.answer_data))
    answer.scoring_data = json.dumps(scoring_data)
    answer.duration = datetime.timedelta(seconds=int(data['duration']))
    answer.submission_time = now
    answer.save()
    answer_set.end_time = now
    return JsonResponse({
        'scoring_data': scoring_data
    })


def get_403_error(message=None):
    if message is None:
        return JsonResponse({}, status=403)
    return JsonResponse({'status_message': message}, status=403)


def get_question(request):
    answer_set = AnswerSet.objects.get(id=request.GET['answer_set_id'])
    question_set = answer_set.question_set
    for i, next_question_id in enumerate(json.loads(question_set.question_ids)):
        if int(request.GET['current_index']) == i + 1:
            break
    else:
        next_question_id = None
    question = Question.objects.get(id=int(request.GET['current_id']))
    return JsonResponse({
        'statement': json.loads(question.statement),
        'type': question.type,
        'max_duration': question.max_duration.seconds,
        'next_index': next_question_id
    })


def get_results(request):
    answer_set = AnswerSet.objects.get(id=request.POST['answer_set_id'])
    answer_set.end_time = datetime.datetime.utcnow()
    answer_set.save()
    return JsonResponse({
        'success': True
    })


def contour_tile(request, question_id):
    question = Question.objects.get(id=int(question_id))
    image = question.map_area.contour_map_image
    return HttpResponse(
        image,
        content_type='image/{}'.format(imghdr.what(None, h=image))
    )


def create_map_area(request, form=False):
    if form:
        display_bounds = {
            'east': int(request.POST['display_east']),
            'north': int(request.POST['display_north']),
            'south': int(request.POST['display_south']),
            'west': int(request.POST['display_west'])
        }
    else:
        display_bounds = json.loads(request.POST['display_area'])
    assert questions.validate_bounds(display_bounds)
    display_area = LatLngBounds()
    display_area.east = display_bounds['east']
    display_area.north = display_bounds['north']
    display_area.south = display_bounds['south']
    display_area.west = display_bounds['west']
    display_area.save()

    if request.POST['contour_east']:
        if form:
            contour_bounds = {
                'east': int(request.POST['contour_east']),
                'north': int(request.POST['contour_north']),
                'south': int(request.POST['contour_south']),
                'west': int(request.POST['contour_west'])
            }
        else:
            contour_bounds = json.loads(request.POST['contour_map_reference'])
        assert questions.validate_bounds(contour_bounds)
        contour_map_reference = LatLngBounds()
        contour_map_reference.east = contour_bounds['east']
        contour_map_reference.north = contour_bounds['north']
        contour_map_reference.south = contour_bounds['south']
        contour_map_reference.west = contour_bounds['west']
        contour_map_reference.save()
    else:
        contour_map_reference = None

    map_area = MapArea()
    map_area.title = request.POST['title']
    assert type(map_area.title) is str
    map_area.display_area = display_area
    map_area.contour_map_reference = contour_map_reference
    if 'contour_map_image' in request.FILES:
        map_area.contour_map_image = list(request.FILES['contour_map_image'].chunks())[0]
    map_area.save()
    return map_area.id


def create_question(request):
    print(request.POST)
    question = Question()
    question.map_area = MapArea.objects.get(id=int(request.POST['map_area_id']))
    question.max_duration = datetime.timedelta(seconds=int(request.POST['max_duration']))
    question.creator = request.user
    question.type = request.POST['type']
    assert type(question.type) is str
    question.statement_data = request.POST['statement_data']
    assert question.actions.validate_statement_data(question.statement_data)
    question.reference_data = request.POST['reference_data']
    assert question.actions.validate_reference_data(question.reference_data)
    question.save()
    return JsonResponse({'question_id': question.id})


def create_question_set(request):
    question_set = QuestionSet()
    question_set.title = request.POST['title']
    assert type(question_set.title) is str
    question_set.creator = request.user
    question_set.max_duration = datetime.timedelta(seconds=request.POST['max_duration'])
    question_set.question_ids = request.POST['question_ids']
    question_ids = json.loads(question_set.question_ids)
    assert type(question_ids) is list
    for question_id in question_ids:
        Question.objects.get(id=question_id)
        assert type(question_id) is int
    question_set.save()
    return JsonResponse({'question_set_id': question_set.id})


def delete_question_set(request):
    QuestionSet.objects.get(id=request.DELETE['question_set_id']).delete()
    return JsonResponse({})


def delete_question(request):
    Question.objects.get(id=request.DELETE['question_id']).delete()
    return JsonResponse({})
