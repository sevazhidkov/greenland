import json
import datetime
import math
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from maps.models import QuestionSet, AnswerSet, Answer


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


def create_answer(request):
    now = datetime.datetime.now();
    answer_set = AnswerSet.objects.get(id=request.POST['answer_set_id'])
    question_set = answer_set.question_set
    if question_set.max_duration > now.__sub__(answer_set.start_time):
        return HttpResponse(json.dumps({
            'status': 'Oops... Too late!'  # TODO
        }))
    question_set_member_index = request.POST['index']
    answer = Answer()
    answer.answer_set = answer_set
    answer.question_set_member = QuestionSetMember.get(question_set__id=question_set.id,
                                                       index=question_set_member_index)
    question = answer.question_set_member.question
    answer.answer_data = request.POST['answer']
    answer.scoring_data = get_scoring_data(question.type, question.reference_data, answer.answer_data)
    answer.duration = now.__sub__(answer_set.end_time)
    answer.submission_time = now
    answer.save()
    answer_set.end_time = now
    return HttpResponse(json.dumps({
        'scoring_data': answer.scoring_data
    }))

EARTH_RADIUS = 6371000


def get_scoring_data(question_type, reference_data, answer_data):
    if question_type == 'point_feature_location':
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
