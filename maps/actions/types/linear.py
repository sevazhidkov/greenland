import json
from maps.actions.types import point
from maps.actions import utils


def get_scoring_data(reference_data, answer_data):
    if answer_data is None:
        return {'correct_location': reference_data['location'], 'hint': reference_data['hint'],
                'score': 0, 'accuracy': None}
    correct_points = reference_data['points']
    answer_points = answer_data['points']
    max_distance = -1
    for correct_point in correct_points:
        min_distance = float('inf')
        for i in range(len(answer_points) - 1):
            lat = correct_point['lat']
            lng = correct_point['lng']
            lat1 = answer_points[i]['lat']
            lng1 = answer_points[i]['lng']
            lat2 = answer_points[i + 1]['lat']
            lng2 = answer_points[i + 1]['lng']
            min_distance = min(min_distance, utils.distance_to_segment(lat, lng, lat1, lng1, lat2, lng2))
        max_distance = max(max_distance, min_distance)
    for answer_point in answer_points:
        min_distance = float('inf')
        for i in range(len(correct_points) - 1):
            lat = answer_point['lat']
            lng = answer_point['lng']
            lat1 = correct_points[i]['lat']
            lng1 = correct_points[i]['lng']
            lat2 = correct_points[i + 1]['lat']
            lng2 = correct_points[i + 1]['lng']
            min_distance = min(min_distance, utils.distance_to_segment(lat, lng, lat1, lng1, lat2, lng2))
        max_distance = max(max_distance, min_distance)
    sufficient_max_distance = reference_data['sufficient_max_distance']
    failed_max_distance = reference_data['failed_max_distance']
    score = min(max(0, failed_max_distance - max_distance) / (failed_max_distance - sufficient_max_distance), 1)
    return {'correct_points': correct_points, 'hint': reference_data['hint'],
            'max_distance': max_distance, 'score': score}


def validate_answer_data(answer_data):
    try:
        answer_data = json.loads(answer_data)
        assert 'points' in answer_data
        points = answer_data['points']
        assert len(points) > 0
        assert len(answer_data) == 1
        for answer_point in points:
            assert 'lat' in answer_point
            lat = answer_point['lat']
            assert 'lng' in answer_point
            lng = answer_point['lng']
            assert len(answer_point) == 2
            assert type(lat) in (float, int)
            assert type(lng) in (float, int)
    except (TypeError, json.JSONDecodeError, AssertionError):
        return False
    else:
        return True


def validate_statement_data(statement_data):
    return point.validate_statement_data(statement_data)


def validate_reference_data(reference_data):
    try:
        reference_data = json.loads(reference_data)
        assert 'points' in reference_data
        points = reference_data['points']
        assert len(points) > 0
        assert len(reference_data) == 4
        for reference_point in points:
            assert 'sufficient_max_distance' in reference_data
            sufficient_max_distance = reference_data['sufficient_max_distance']
            assert 'failed_max_distance' in reference_data
            failed_max_distance = reference_data['failed_max_distance']
            assert 'hint' in reference_data
            hint = reference_data['hint']
            assert 'lat' in reference_point
            lat = reference_point['lat']
            assert 'lng' in reference_point
            lng = reference_point['lng']
            assert len(reference_point) == 2
            assert type(lat) in (float, int)
            assert type(lng) in (float, int)
        assert type(sufficient_max_distance) in (float, int)
        assert type(failed_max_distance) in (float, int)
        assert type(hint) in str
    except (TypeError, json.JSONDecodeError, AssertionError):
        return False
    else:
        return True
