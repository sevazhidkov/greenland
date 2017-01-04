import json
import math

from maps.models import QuestionSet, AnswerSet


def question_set_list():
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


def create_answer_set(user, question_set_id):
    obj = AnswerSet()
    obj.student = user
    obj.question_set = QuestionSet.objects.get(id=question_set_id)
    obj.start_time = datetime.datetime.utcnow()
    obj.save()
    return obj


EARTH_RADIUS = 6371000
POINT_FEATURE_LOCATION = 'point_feature_location'


def get_scoring_data(question_type, reference_data, answer_data):
    if question_type == POINT_FEATURE_LOCATION:
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


def validate_answer_data(question_type, answer_data):
    if question_type != POINT_FEATURE_LOCATION:
        return NotImplemented
    try:
        answer_data = json.loads(answer_data)
        assert 'location' in answer_data
        location = answer_data['location']
        assert len(answer_data) == 1
        assert 'lat' in location
        lat = location['lat']
        assert 'lng' in location
        lng = location['lng']
        assert len(location) == 2
        assert type(lat) in (float, int)
        assert type(lng) in (float, int)
    except (TypeError, json.JSONDecodeError, AssertionError):
        return False
    else:
        return True


def validate_statement_data(question_type, statement_data):
    if question_type != POINT_FEATURE_LOCATION:
        return NotImplemented
    try:
        statement_data = json.loads(statement_data)
        assert 'name' in statement_data
        assert len(statement_data) == 1
        assert type(statement_data['name']) is str
    except (TypeError, json.JSONDecodeError, AssertionError):
        return False
    else:
        return True


def validate_reference_data(question_type, reference_data):
    if question_type != POINT_FEATURE_LOCATION:
        return NotImplemented
    try:
        reference_data = json.loads(reference_data)
        assert 'location' in reference_data
        location = reference_data['location']
        assert 'sufficient_accuracy' in reference_data
        sufficient_accuracy = reference_data['sufficient_accuracy']
        assert 'failed_accuracy' in reference_data
        failed_accuracy = reference_data['failed_accuracy']
        assert 'hint' in reference_data
        hint = reference_data['hint']
        assert len(reference_data) == 4
        assert 'lat' in location
        lat = location['lat']
        assert 'lng' in location
        lng = location['lng']
        assert len(location) == 2
        assert type(lat) in (float, int)
        assert type(lng) in (float, int)
        assert type(sufficient_accuracy) in (float, int)
        assert type(failed_accuracy) in (float, int)
        assert type(hint) in str
    except (TypeError, json.JSONDecodeError, AssertionError):
        return False
    else:
        return True