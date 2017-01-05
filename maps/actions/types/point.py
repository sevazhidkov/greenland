import json
from maps.actions import questions

EARTH_RADIUS = 6371000
POINT_FEATURE_LOCATION = 'point_feature_location'


def get_scoring_data(reference_data, answer_data):
    if answer_data is None:
        return {'correct_location': reference_data['location'], 'hint': reference_data['hint'],
                'score': 0, 'accuracy': None}
    correct_location = reference_data['location']
    answer_location = answer_data['location']
    lat1 = correct_location['lat']
    lng1 = correct_location['lng']
    lat2 = answer_location['lat']
    lng2 = answer_location['lng']
    accuracy = questions.distance(lat1, lng1, lat2, lng2)
    sufficient_accuracy = reference_data['sufficient_accuracy']
    failed_accuracy = reference_data['failed_accuracy']
    score = min(max(0, failed_accuracy - accuracy) / (failed_accuracy - sufficient_accuracy), 1)
    return {'correct_location': correct_location, 'hint': reference_data['hint'],
            'accuracy': accuracy, 'score': score}


def validate_answer_data(answer_data):
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


def validate_statement_data(statement_data):
    try:
        statement_data = json.loads(statement_data)
        assert 'name' in statement_data
        assert len(statement_data) == 1
        assert type(statement_data['name']) is str
    except (TypeError, json.JSONDecodeError, AssertionError):
        return False
    else:
        return True


def validate_reference_data(reference_data):
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
        assert type(hint) in [str]
    except (TypeError, json.JSONDecodeError, AssertionError) as error:
        print(error)
        return False
    else:
        return True
