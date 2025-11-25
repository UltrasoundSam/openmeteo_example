import pytest
import datetime as dt

from openmeteo_example import MeteoForecast


VALID_LOCATION = (12.38, -8)
INVALID_LATITUDE = (100, -18)
INVALID_LONGITUDE = (-60, 270)


@pytest.fixture
def valid_object() -> MeteoForecast:
    test = MeteoForecast(*VALID_LOCATION)
    return test


def test_instantiation(valid_object: MeteoForecast):
    '''Tests that object can be correctly instantiated'''

    assert isinstance(valid_object, MeteoForecast)


@pytest.mark.parametrize("location",
                         [INVALID_LATITUDE,
                          INVALID_LONGITUDE])
def test_invalid_position(location: tuple[float, float]):
    with pytest.raises(ValueError):
        _ = MeteoForecast(*location)


@pytest.mark.parametrize("parameter, param_type",
                         [('temperature', float),
                          ('wind', float),
                          ('cloud', int),
                          ('precipitation', float)])
def test_properties(valid_object, parameter, param_type):
    '''Test that we can get parameters and that they are
    of the correct type
    '''
    dt_array, param_array = getattr(valid_object, parameter)

    assert all(isinstance(datum, param_type) for datum in param_array)
    assert all(isinstance(datum, dt.datetime) for datum in dt_array)


def test_location(valid_object):
    '''Tests that location is set correctly'''
    assert valid_object.latitude == VALID_LOCATION[0]
    assert valid_object.longitude == VALID_LOCATION[1]


def test_elevation(valid_object):
    '''Tests that elevation has correct type'''
    assert isinstance(valid_object.elevation, float)


def test_current_data(valid_object):
    '''Tests that we can get current data (make sure it returns
    a dictionary with a 'current' key'''
    assert valid_object.get_current_data()['current']
