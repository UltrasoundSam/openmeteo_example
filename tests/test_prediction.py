import pytest
import datetime as dt
import torch
import random

from openmeteo_example import MeteoHistorical
from openmeteo_example.prediction import WeatherPredictor


YORK_LOCATION = (53.958332, -1.080278)

# Create start and end dates
START_DATE = dt.datetime(2020, 1, 1, 0, 1)
END_DATE = dt.datetime(2020, 1, 31, 23, 59)
MID_MONTH = dt.datetime(2020, 1, 20)
month = [dt.datetime(2020, 1, day + 1) for day in range(31)]
random_days = random.sample(month, 5)


@pytest.fixture(scope="session")
def york_location_data() -> MeteoHistorical:
    """Defines York location meteo historic as a fixture
    to allow reuse of object
    """
    york = MeteoHistorical(*YORK_LOCATION)
    york.get_data(START_DATE, END_DATE)
    return york


@pytest.fixture()
def york_prediction(york_location_data: MeteoHistorical) -> WeatherPredictor:
    """Defines WeatherPredictor object as fixture to
    reused object during testing
    """
    predictor = WeatherPredictor(york_location_data)
    return predictor


def test_weather(
    york_location_data: MeteoHistorical, york_prediction: WeatherPredictor
):
    """Tests that weather data is assimilated into predictor"""
    assert york_prediction.weather is york_location_data


@pytest.mark.parametrize("day", random_days)
def test_label_select_type(york_prediction: WeatherPredictor, day: dt.datetime):
    """Tests that training label (temperature over 24 hour
    period) is extracted as correct type
    """
    labels = york_prediction._select_label_data(day)
    assert isinstance(labels, torch.Tensor)


@pytest.mark.parametrize("day", random_days)
def test_label_select_value(
    york_prediction: WeatherPredictor,
    york_location_data: MeteoHistorical,
    day: dt.datetime,
):
    """Tests that training label (temperature over 24 hour
    period) is extracted as correct type
    """
    # Get labels from class
    labels = york_prediction._select_label_data(day)

    # Get labels from source
    temp_dates, temp_values = york_location_data.temperature
    indx = temp_dates.index(day)
    temp_tensor = torch.Tensor(temp_values[indx : indx + 24])

    assert torch.equal(labels, temp_tensor)


def test_training_select(york_prediction: WeatherPredictor):
    """Makes sure data is selected correctly"""
    # Get training data
    training_data = york_prediction._select_training_data(MID_MONTH)

    # Get first day of training data
    temp_days, temp_values = york_prediction.weather.temperature
    start_day = MID_MONTH - dt.timedelta(days=7)
    start_indx = temp_days.index(start_day)

    assert training_data[0] == temp_values[start_indx]

    # Check last value of tensor
    wind = york_prediction.weather.wind[1]
    end_indx = temp_days.index(MID_MONTH) - 1
    assert training_data[-1] == wind[end_indx]
