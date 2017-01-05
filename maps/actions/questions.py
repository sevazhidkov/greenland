import json
import math
import datetime
import json
from maps.models import QuestionSet, AnswerSet, Question, MapArea


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


def map_area_list():
    return list(map(lambda m: {'id': m.id, 'title': m.title}, MapArea.objects.all()))


def create_answer_set(user, question_set_id):
    obj = AnswerSet()
    obj.student = user
    obj.question_set = QuestionSet.objects.get(id=question_set_id)
    obj.start_time = datetime.datetime.utcnow()
    obj.save()
    return obj


def validate_bounds(bounds):
    try:
        assert 'east' in bounds
        assert 'north' in bounds
        assert 'south' in bounds
        assert 'west' in bounds
        assert type(bounds['east']) in (float, int)
        assert type(bounds['north']) in (float, int)
        assert type(bounds['south']) in (float, int)
        assert type(bounds['west']) in (float, int)
    except AssertionError:
        return False
    else:
        return True


def get_type(name):
    pass
