import csv
import io
import itertools
from geopy import distance
from geopy.geocoders import Nominatim


def get_data_csv(f):
    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    next(csv_input)
    return [row for row in csv_input]


def geo_reverse(lat: float, lon: float) -> str:
    """
    Get the name of a place by latitude and longitude
    """
    geo = f"{lat}, {lon}"
    geolocator = Nominatim(user_agent="test")
    location = geolocator.reverse(geo)
    return location.address


def all_subsets(lst):
    """
    all combinations of two items from the list
    """
    return itertools.chain(*map(lambda x: itertools.combinations(lst, x), range(2, 3)))


def distance_meters(geo1, geo2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    return round(distance.distance(geo1, geo2).meters, 1)
