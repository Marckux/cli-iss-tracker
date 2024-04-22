import math
from datetime import time

R = 6371  # Radius of the Earth in Km


def magnitude(v: tuple) -> float:
    """
    Calculate the magnitude of a vector
    :param v: tuple of n elements
    :return: float
    """
    return math.sqrt(sum([a ** 2 for a in v]))


def dot_product(v: tuple, w: tuple) -> float:
    """
    Calculate the dot product of two vectors
    :param v: tuple of n elements
    :param w: tuple of n elements
    :return: float
    :throws ValueError if the vectors have different lengths
    """
    if len(v) != len(w):
        raise ValueError('Vectors must have the same length')
    return sum([a * b for a, b in zip(v, w)])


def cross_product(v: tuple, w: tuple) -> tuple:
    """
    Calculate the cross product of two vectors
    :param v: tuple of 3 elements
    :param w: tuple of 3 elements
    :return: tuple of 3 elements (x, y, z) perpendicular to the plane formed by v and w
    :throws ValueError if any vector has a different length than 3
    """
    if len(v) != 3 or len(w) != 3:
        raise ValueError('Vectors must have a length of 3')
    x = v[1] * w[2] - v[2] * w[1]
    y = v[2] * w[0] - v[0] * w[2]
    z = v[0] * w[1] - v[1] * w[0]
    return x, y, z


def to_vector(lat: float, long: float) -> tuple:
    """
    Convert latitude and longitude to a vector
    :param lat: float latitude in degrees (-90.0 to 90.0)
    :param long: float longitude in degrees (-180.0 to 180.0)
    :return: tuple of 3 elements (x, y, z) in Km from the center of the Earth
    :throws ValueError if the latitude or longitude are out of range
    """
    if lat < -90 or lat > 90:
        raise ValueError('Latitude must be between -90 and 90')
    if long < -180 or long > 180:
        raise ValueError('Longitude must be between -180 and 180')
    x = R * math.cos(math.radians(lat)) * math.cos(math.radians(long))
    y = R * math.cos(math.radians(lat)) * math.sin(math.radians(long))
    z = R * math.sin(math.radians(lat))
    return x, y, z


def angle_vectors(v: tuple, w: tuple) -> float:
    """
    Calculate the angle between two vectors in radians
    :param v: tuple of n elements
    :param w: tuple of n elements
    :return: float angle in radians
    :throws ValueError if the vectors have different lengths
    """
    if len(v) != len(w):
        raise ValueError('Vectors must have the same length')
    if magnitude(v) == 0 or magnitude(w) == 0:
        return 0
    return math.acos(round(dot_product(v, w) / (magnitude(v) * magnitude(w)), 5))


def angle_between_coordinates(lat1: float, long1: float, lat2: float, long2: float) -> float:
    """
    Calculate the angle between two coordinates in radians
    :param lat1: float latitude in degrees (-90.0 to 90.0)
    :param long1: float longitude in degrees (-180.0 to 180.0)
    :param lat2: float latitude in degrees (-90.0 to 90.0)
    :param long2: float longitude in degrees (-180.0 to 180.0)
    :return: float angle in radians
    :throws ValueError if the latitude or longitude are out of range
    """
    u = to_vector(lat1, long1)
    v = to_vector(lat2, long2)
    return angle_vectors(u, v)


def distance_between_coordinates(lat1: float, long1: float, lat2: float, long2: float) -> float:
    """
    Calculate the distance between two coordinates
    :param lat1: float latitude in degrees (-90.0 to 90.0)
    :param long1: float longitude in degrees (-180.0 to 180.0)
    :param lat2: float latitude in degrees (-90.0 to 90.0)
    :param long2: float longitude in degrees (-180.0 to 180.0)
    :return: float distance in Km
    :throws ValueError if the latitude or longitude are out of range
    """
    angle = angle_between_coordinates(lat1, long1, lat2, long2)
    return angle * R


def direction_between_coordinates(lat1: float, long1: float, lat2: float, long2: float) -> tuple:
    """
    Calculate the direction between two coordinates
    :param lat1: float latitude in degrees (-90.0 to 90.0)
    :param long1: float longitude in degrees (-180.0 to 180.0)
    :param lat2: float latitude in degrees (-90.0 to 90.0)
    :param long2: float longitude in degrees (-180.0 to 180.0)
    :return: tuple of 3 elements (x, y, z) that points from the first to the second coordinate
    over the surface of the Earth
    :throws ValueError if the latitude or longitude are out of range
    """
    v = to_vector(lat1, long1)
    w = to_vector(lat2, long2)
    result = cross_product(cross_product(v, w), v)
    if magnitude(result) < 1:
        return cross_product(cross_product(v, (0, 0, 1)), v)
    else:
        return result


def bearing_between_coordinates(lat1: float, long1: float, lat2: float, long2: float) -> float:
    """
    Calculate the bearing between two coordinates
    :param lat1: float latitude in degrees (-90.0 to 90.0)
    :param long1: float longitude in degrees (-180.0 to 180.0)
    :param lat2: float latitude in degrees (-90.0 to 90.0)
    :param long2: float longitude in degrees (-180.0 to 180.0)
    :return: float bearing in degrees
    """
    v = to_vector(lat1, long1)
    north_vector = cross_product(cross_product(v, (0, 0, 1)), v)
    w = direction_between_coordinates(lat1, long1, lat2, long2)
    bearing = math.degrees(angle_vectors(w, north_vector))
    if long2 < long1:
        bearing = 360 - bearing
    return bearing


def cardinal_from_angle(angle: float) -> str:
    """
    Get the cardinal direction from an angle
    :param angle: float angle in degrees (0 to 360) where 0 is North
    :return: str cardinal direction
    """
    cardinals = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N']
    return cardinals[round(angle / 45)]

