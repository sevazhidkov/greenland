import math

EARTH_RADIUS = 6371000
EPS = 1e-4


def distance(lat1, lng1, lat2, lng2):
    return EARTH_RADIUS * angle_distance(lat1, lng1, lat2, lng2)


def angle_distance(lat1, lng1, lat2, lng2):
    return 2 * math.asin((1 - math.cos(lat1) * math.cos(lat2) - math.sin(lat1) * math.sin(lat2) *
                          math.cos(lng1 - lng2)) / 2)


def distance_to_segment(lat, lng, lat1, lng1, lat2, lng2):
    d2 = angle_distance(distance(lat, lng, lat1, lng1))
    d1 = angle_distance(distance(lat, lng, lat2, lng2))
    d = angle_distance(distance(lat1, lng1, lat2, lng2))
    a1 = (math.cos(d1) - math.cos(d2) * math.cos(d)) / math.sin(d2) / math.sin(d)
    a2 = (math.cos(d2) - math.cos(d1) * math.cos(d)) / math.sin(d1) / math.sin(d)
    if a1 > math.pi / 2 or a2 > math.pi / 2:
        return EARTH_RADIUS * min(d1, d2)
    c = math.asin(math.sin(d1) * math.sin(a2))
    if c > math.pi / 2 and c <= math.pi + EPS:
        c = math.pi - c
    return EARTH_RADIUS * c
