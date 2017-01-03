import json
import datetime
import math
from django.http import JsonResponse
from maps.models import QuestionSet, AnswerSet, Answer, Question


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
    return JsonResponse(list_question_sets())


def create_answer_set(user, question_set_id):
    obj = AnswerSet()
    obj.student = user
    obj.question_set = QuestionSet.objects.get(id=question_set_id)
    obj.start_time = datetime.datetime.utcnow()
    obj.save()
    return obj


def http_create_answer_set(request):
    obj = create_answer_set(request.user, request.POST['question_set_id'])
    return JsonResponse({
        'answer_set_id': obj.id,
        'start_index': 0,
        'max_duration': obj.question_set.max_duration.seconds
    })


def create_answer(request):
    now = datetime.datetime.utcnow()
    answer_set = AnswerSet.objects.get(id=request.POST['answer_set_id'])
    question_set = answer_set.question_set
    if question_set.max_duration.seconds < now.timestamp() - answer_set.start_time.timestamp():
        return JsonResponse({
            'status_message': 'Test is already over',
        }, status=403)
    question_index = int(request.POST['index'])
    answer = Answer()
    answer.answer_set = answer_set
    answer.question_set = question_set
    answer.question = Question.objects.get(id=json.loads(question_set.question_ids)[question_index])
    if 'answer' in request.POST:
        answer.answer_data = request.POST['answer']
    answer.scoring_data = json.dumps(get_scoring_data(answer.question.type,
                                                      json.loads(answer.question.reference_data),
                                                      json.loads(answer.answer_data)))
    answer.duration = datetime.timedelta(seconds=int(request.POST['duration']))
    answer.submission_time = now
    answer.save()
    answer_set.end_time = now
    return JsonResponse({
        'scoring_data': answer.scoring_data
    })


EARTH_RADIUS = 6371000


def get_scoring_data(question_type, reference_data, answer_data):
    if question_type == 'point_feature_location':
        if answer_data is None:
            return {'correct_location': reference_data['location'], 'hint': reference_data['hint'],
                    'score': 0, 'accuracy': None}
        correct_location = reference_data['location']
        answer_location = answer_data['location']
        lat1 = correct_location['lat']
        lng1 = correct_location['lng']
        lat2 = answer_location['lat']
        lng2 = answer_location['lng']
        accuracy = 2 * EARTH_RADIUS * math.asin((1 - math.cos(lat1) * math.cos(lat2) - math.sin(lat1) * math.sin(lat2) *
                                                 math.cos(lng1 - lng2)) / 2)
        sufficient_accuracy = reference_data['sufficient_accuracy']
        failed_accuracy = reference_data['failed_accuracy']
        score = max(min(0, accuracy - failed_accuracy) / (sufficient_accuracy - failed_accuracy), 1)
        return {'correct_location': correct_location, 'hint': reference_data['hint'],
                'accuracy': accuracy, 'score': score}
    return NotImplemented


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
