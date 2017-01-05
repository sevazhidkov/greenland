import math

EARTH_RADIUS = 6371000


def distance(lat1, lng1, lat2, lng2):
    return 2 * EARTH_RADIUS * math.asin((1 - math.cos(lat1) * math.cos(lat2) - math.sin(lat1) * math.sin(lat2) *
                                        math.cos(lng1 - lng2)) / 2)
