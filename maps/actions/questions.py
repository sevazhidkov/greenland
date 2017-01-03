import math
import datetime
import json
from maps.models import QuestionSet, AnswerSet, Question


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


def pretty_display_area(area):
    return 'N: ' + str(area.north) + ', S: ' + str(area.south) + '<br>' \
           + 'W: ' + str(area.west) + ', E: ' + str(area.east)


def question_set_list():
    return list(map(lambda q:
                    {'id': q.id, 'title': q.title, 'creator': q.creator.get_full_name(),
                     'duration': pretty_duration(q.max_duration.seconds)},
                    QuestionSet.objects.all()))


def question_list():
    return list(map(lambda q: {'id': q.id, 'statement_data': json.loads(q.statement_data), 'type': q.type,
                               'duration': pretty_duration(q.max_duration.seconds),
                               'creator': q.creator.get_full_name(),
                               'map_area': pretty_display_area(q.map_area.display_area)},
                    Question.objects.all()))


def create_answer_set(user, question_set_id):
    obj = AnswerSet()
    obj.student = user
    obj.question_set = QuestionSet.objects.get(id=question_set_id)
    obj.start_time = datetime.datetime.utcnow()
    obj.save()
    return obj


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
