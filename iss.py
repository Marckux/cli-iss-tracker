# Description: This script will get the current location of the ISS
from math import sqrt, cos, asin, sin, pi, degrees

import requests
import geo
from datetime import datetime


def elevation(alpha: float) -> float:
    """
    Returns the elevation angle in degrees of the ISS
    :param alpha: float, the angle between points on the earth
    :return: float: elevation angle in degrees
    """
    r = 6371  # The radius of Earth in Km
    h = 408  # The high of the ISS
    distance = sqrt(r ** 2 + (r+h) ** 2 - 2 * r * (r+h) * cos(alpha))  # Law of cosines
    gamma = asin(sin(alpha)*r/distance)  # Law of sines
    return degrees(pi/2 - alpha - gamma)


def to_timestamp(utc_time: str) -> int:
    """
    Convert a UTC time to a timestamp
    :param utc_time: str, time in the format 'HH:MM:SS AM/PM'
    :return: int, timestamp in seconds
    """
    today = datetime.utcnow()
    time = (datetime
            .strptime(utc_time, '%I:%M:%S %p')
            .replace(year=today.year, month=today.month, day=today.day))
    return int(time.timestamp())


def is_nighttime(sunrise: str, sunset: str) -> bool:
    """
    Check if it is nighttime
    :param sunrise: str, time in the format 'HH:MM:SS AM/PM'
    :param sunset: str, time in the format 'HH:MM:SS AM/PM'
    :return: bool, True if it is nighttime, False otherwise
    """
    now = datetime.utcnow().timestamp()
    sunrise_time = to_timestamp(sunrise)
    sunset_time = to_timestamp(sunset)
    return now < sunrise_time or now > sunset_time


# Make a get request to get the latest position of the international space station from the open notify api
url_iss = "http://api.open-notify.org/iss-now.json"
url_sun = "https://api.sunrise-sunset.org/json"
my_latitude = 38.511883729973015
my_longitude = -0.23174407854098136

try:
    response_iss = requests.get(url_iss)
    response_iss.raise_for_status()
    response_sun = requests.get(url_sun, params={'lat': my_latitude, 'lng': my_longitude})
    response_sun.raise_for_status()
    iss_latitude = float(response_iss.json()['iss_position']['latitude'])
    iss_longitude = float(response_iss.json()['iss_position']['longitude'])
    sunrise = response_sun.json()['results']['sunrise']
    sunset = response_sun.json()['results']['sunset']
    angle = geo.angle_between_coordinates(my_latitude, my_longitude, iss_latitude, iss_longitude)
    elevation_angle = elevation(angle)
    azimuth = geo.bearing_between_coordinates(my_latitude, my_longitude, iss_latitude, iss_longitude)
    cardinal = geo.cardinal_from_angle(azimuth)
    is_over_horizon = elevation_angle > 0
    is_dark = is_nighttime(sunrise, sunset)
    print(f'UTC TIME: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'UTC SUNRISE: {sunrise}')
    print(f'UTC SUNSET: {sunset}')
    print(f'Is {"Nighttime" if is_dark else "Daytime"}')
    print(f'MY LOCATION: Latitude {my_latitude:.2f}, Longitude {my_longitude:.2f}')
    print(f'ISS LOCATION: Latitude {iss_latitude:.2f}, Longitude {iss_longitude:.2f}')
    print(f'DISTANCE TO ISS: {geo.distance_between_coordinates(my_latitude, my_longitude, iss_latitude, iss_longitude):.2f} Km')
    print(f'AZIMUTH: {azimuth:.2f} degrees')
    print(f'ELEVATION ANGLE: {elevation_angle:.2f} degrees')
    if not is_dark:
        print(f'Sorry! You cannot see the ISS because it is daytime')
    elif not is_over_horizon:
        print(f'Sorry! You cannot see the ISS because it is below the horizon')
    else:
        print(f'Hurry! The ISS is above the horizon and you can see it!')
        print(f'The azimuth is {azimuth:.2f} degrees. Look to the ({cardinal})')
        print(f'The elevation angle is {elevation_angle:.2f} degrees')

except requests.HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except ValueError as val_err:
    print(f'Value error occurred: {val_err}')
except Exception as err:
    print(f'Something went wrong: {err}')
