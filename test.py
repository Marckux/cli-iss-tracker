import unittest
import geo
import math
import iss
from datetime import datetime


class TestGeo(unittest.TestCase):
    def test_magnitude(self):
        self.assertEqual(geo.magnitude((3, 4)), 5)
        self.assertEqual(geo.magnitude((0, 0)), 0)
        self.assertAlmostEqual(geo.magnitude((1, 1, 1)), 1.7320508075688772)

    def test_dot_product(self):
        self.assertAlmostEqual(geo.dot_product((1, 2), (3, 4)), 11)
        self.assertAlmostEqual(geo.dot_product((1, 1, 1), (1, 1, 1)), 3)

    def test_cross_product(self):
        self.assertEqual(geo.cross_product((1, 0, 0), (0, 1, 0)), (0, 0, 1))
        self.assertEqual(geo.cross_product((1, 1, 1), (1, 1, 1)), (0, 0, 0))

    def test_to_vector(self):
        cases = [
            (0, 0, (6371, 0, 0)),
            (0, 90, (0, 6371, 0)),
            (90, 0, (0, 0, 6371)),
            (90, 90, (0, 0, 6371)),
            (15, -28, (5433.58, -2889.09, 1648.94))

        ]
        for lat, long, expected in cases:
            calculated = geo.to_vector(lat, long)
            for c, e in zip(calculated, expected):
                self.assertAlmostEqual(c, e, places=1)

    def test_angle_vectors(self):
        cases = [
            ((1, 0, 0), (0, 1, 0), 90 * math.pi / 180),
            ((1, 0, 0), (1, 0, 0), 0 * math.pi / 180),
            ((1, 0, 0), (-1, 0, 0), 180 * math.pi / 180),
            ((1, 0, 0), (0, 0, 1), 90 * math.pi / 180),
            ((1, 0, 0), (0, 1, 0), 90 * math.pi / 180),
            ((1, 0, 0), (1, 1, 1), 54.74 * math.pi / 180),
            ((-2, -5, 7), (1, 2, 3), 74.2 * math.pi / 180)
        ]
        for v, w, expected in cases:
            self.assertAlmostEqual(geo.angle_vectors(v, w), expected, places=1)

    def test_angle_between_coordinates(self):
        cases = [
            (0, 0, 0, 0, 0),
            (0, 0, 0, 90, math.pi / 2),
            (0, 0, 0, 180, math.pi),
            (45, 0, 45, 90, math.pi / 3),
            (45, 0, 45, -90, math.pi / 3)
        ]
        for lat1, long1, lat2, long2, expected in cases:
            self.assertAlmostEqual(geo.angle_between_coordinates(lat1, long1, lat2, long2), expected, places=1)

    def test_distance_between_coordinates(self):
        cases = [
            (0, 0, 0, 0, 0),
            (0, 0, 0, 90, 10007.54),
            (0, 0, 0, 180, 20015.09),
            (45, 0, 45, 90, 6671.70),
            (45, 0, 45, -90, 6671.70)
        ]
        for lat1, long1, lat2, long2, expected in cases:
            self.assertAlmostEqual(geo.distance_between_coordinates(lat1, long1, lat2, long2), expected, places=1)

    def test_direction_between_coordinates(self):
        cases = [
            (0, 0, 0, 0, (0, 0, 40589641.0)),
            (0, 0, 0, 90, (0, 258596602811.0, 0)),
            (0, 0, 0, 180, (0, 0, 40589641.0)),
            (45, 0, 45, 90, (-91427705719.73, 182855411439.46, 91427705719.73))
        ]
        for lat1, long1, lat2, long2, expected in cases:
            calculated = geo.direction_between_coordinates(lat1, long1, lat2, long2)
            for c, e in zip(calculated, expected):
                self.assertAlmostEqual(c, e, places=1)

    def test_bearing_between_coordinates(self):
        cases = [
            (0, 0, 0, 0, 0),
            (0, 0, 0, 90, 90),
            (0, 0, 0, 180, 0),
            (45, 0, 45, 90, 54.74),
            (45, 0, 45, -90, 305.26)
        ]
        for lat1, long1, lat2, long2, expected in cases:
            self.assertAlmostEqual(geo.bearing_between_coordinates(lat1, long1, lat2, long2), expected, places=1)

    def test_cardinal_from_angle(self):
        cases = [
            (0, 'N'),
            (90, 'E'),
            (180, 'S'),
            (270, 'W'),
            (45, 'NE'),
            (135, 'SE'),
            (225, 'SW'),
            (315, 'NW')
        ]
        for angle, expected in cases:
            self.assertEqual(geo.cardinal_from_angle(angle), expected)


class TestIss(unittest.TestCase):
    def test_elevation(self):
        cases = [
            (10 * math.pi / 180, 14.53),
            (0, 90)
        ]
        for alpha, expected in cases:
            self.assertAlmostEqual(iss.elevation(alpha), expected, places=1)

    def test_to_timestamp(self):
        cases = [
            ('12:00:00 AM', 0),
            ('12:00:00 PM', 43200),
            ('06:00:00 AM', 21600),
            ('06:00:00 PM', 64800)
        ]
        today = datetime.utcnow()
        for time, expected in cases:
            calculated = iss.to_timestamp(time)
            time = (datetime
                    .strptime(time, '%I:%M:%S %p')
                    .replace(year=today.year, month=today.month, day=today.day))
            self.assertEqual(calculated, int(time.timestamp()))
