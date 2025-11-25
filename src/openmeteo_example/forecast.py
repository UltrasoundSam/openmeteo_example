# -*- coding: utf-8 -*-
"""
Created on Tues November 25 2025 11:30

@author: samhill

This file creates the MeteoForecast class that encapsulates everything to do
with forecast data from OpenMeteo
"""
import datetime as dt
import requests
from typing import Optional

from .openmeteo import OpenMeteo


class MeteoForecast(OpenMeteo):
    base_url = 'https://api.open-meteo.com/v1/forecast'

    def __init__(self,
                 latitude: float,
                 longitude: float) -> None:

        super().__init__(latitude, longitude)

        # Get current data
        data = self.get_current_data()

        # Parse date
        date = dt.datetime.fromisoformat(data['current']['time'])

        # Process measurement data
        for key in self._measures:
            self._parse_current_measurement(key,
                                            data,
                                            date)

        # Define elevation value (if useful)
        self.__elevation = data["elevation"]

    @property
    def elevation(self) -> int:
        '''Returns elevation according to API
        '''
        return self.__elevation

    def get_current_data(self) -> dict:
        '''Get current data from API. This will be everything in the
        _measureas dictionary
        '''
        # Get all measurements
        meas = ','.join(self._measures.values())

        # Request values
        request_info = {'latitude': self.latitude,
                        'longitude': self.longitude,
                        'current': meas}

        # Format API endpoint
        url = requests.get(self.base_url,
                           params=request_info)

        # Get response info
        data = url.json()

        return data

    def _parse_current_measurement(self,
                                   data_name: str,
                                   json_payload: dict,
                                   date: dt.datetime) -> None:
        '''Parses json object data and puts it into object data
        storage
        '''
        # Get object and api names
        obj_name = data_name
        api_name = self._measures[data_name]

        # Add in measurement unit
        unit = json_payload['current_units'][api_name]
        self._data[obj_name]['unit'] = unit

        # Add in measurement time
        self._data[obj_name]['time'].append(date)

        # Get in measurements
        data = json_payload['current'][api_name]
        self._data[obj_name]['data'].append(data)

    def get_data(self,
                 end_date: Optional[dt.datetime] = None,
                 temperature: bool = True,
                 wind_speed: bool = True,
                 cloud_cover: bool = True,
                 precipitation: bool = True):
        '''Refining get data method for forecast API'''

        start_date = dt.datetime.now()
        if end_date is None:
            # Check a week into the future
            end_date = start_date + dt.timedelta(days=7)

        super().get_data(start_date=start_date,
                         end_date=end_date,
                         temperature=temperature,
                         wind_speed=wind_speed,
                         cloud_cover=cloud_cover,
                         precipitation=precipitation)
