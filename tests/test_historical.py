import pytest

from openmeteo_example import MeteoHistorical


VALID_LOCATION = (12.38, -8)
INVALID_LATITUDE = (100, -18)
INVALID_LONGITUDE = (-60, 270)


def test_instantiation():
    """Tests that object can be correctly instantiated"""

    test = MeteoHistorical(*VALID_LOCATION)
    assert isinstance(test, MeteoHistorical)


@pytest.mark.parametrize("location", [INVALID_LATITUDE, INVALID_LONGITUDE])
def test_invalid_position(location):
    with pytest.raises(ValueError):
        _ = MeteoHistorical(*location)
