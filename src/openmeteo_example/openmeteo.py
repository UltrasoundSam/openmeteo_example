# -*- coding: utf-8 -*-
"""
Created on Tues November 25 2025 10:44

@author: samhill

This file creates the abstract base class OpenMeteo to take care of
consistent attributes and methods shared between historic and forecast
classes
"""

import datetime as dt
import requests
from typing import Optional
from collections import defaultdict
from abc import ABC
from enum import Flag, auto


class MeasType(Flag):
    TEMPERATURE = auto()
    CLOUD = auto()
    PRECIPITATION = auto()
    WIND = auto()


class OpenMeteo(ABC):
    # Base URL of the API
    base_url = "https://api.open-meteo.com/v1/"

    # Useful look-up for API terms
    _measures = {
        MeasType.TEMPERATURE: "temperature_2m",
        MeasType.CLOUD: "cloud_cover",
        MeasType.PRECIPITATION: "precipitation",
        MeasType.WIND: "wind_speed_10m",
    }

    def __init__(self, latitude: float, longitude: float) -> None:
        """Initialises object by assigning latitude
        and longitude of location to object. These should be
        fixed and unchanged after initialisation.

        Inputs:
            Latitude [float]      - Latitude of location in degrees
            Longitude [float]     - Longitude of location in degrees

        Returns:
            None
        """
        # Assign latitude and longitude - assuming they are in valid range
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90 Degrees")

        if not -180 <= longitude <= 180:
            msg = "Longitude must be between -180 and 180 Degrees"
            raise ValueError(msg)

        self.__latitude = latitude
        self.__longitude = longitude

        # Create dictionary to hold data
        self._data = {key: defaultdict(list) for key in self._measures}

    @property
    def latitude(self) -> float:
        return self.__latitude

    @property
    def longitude(self) -> float:
        return self.__longitude

    @property
    def temperature(self) -> Optional[tuple[list[dt.datetime], list[float]]]:
        """Returns temperature data (if any)"""
        return self._return_data(MeasType.TEMPERATURE)

    @property
    def wind(self) -> Optional[tuple[list[dt.datetime], list[float]]]:
        """Returns wind data (if any)"""
        return self._return_data(MeasType.WIND)

    @property
    def cloud(self) -> Optional[tuple[list[dt.datetime], list[int]]]:
        """Returns cloud data (if any)"""
        return self._return_data(MeasType.CLOUD)

    @property
    def precipitation(self) -> Optional[tuple[list[dt.datetime], list[float]]]:
        """Returns cloud data (if any)"""
        return self._return_data(MeasType.PRECIPITATION)

    def get_data(
        self,
        start_date: Optional[dt.datetime] = None,
        end_date: Optional[dt.datetime] = None,
        measurements: MeasType = MeasType(15),
    ) -> None:
        """Get multiple hourly measurements from forecast, up to 16 days in
        advance
        """

        # Get all measurements
        meas = []

        for measurement in measurements:
            meas.append(self._measures[measurement])

        meas = ",".join(meas)

        # Request values
        request_info = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "start_date": start_date.isoformat().split("T")[0],
            "end_date": end_date.isoformat().split("T")[0],
            "hourly": meas,
        }

        # Format API end-point
        results = requests.get(self.base_url, params=request_info)
        results = results.json()

        # Now let's process this data
        time_info = results["hourly"]["time"]
        time_obj = [dt.datetime.fromisoformat(dtstr) for dtstr in time_info]

        for obj_name, api_name in self._measures.items():
            try:
                # Add in time information
                self._data[obj_name]["time"].extend(time_obj)

                # Get measurement values
                values = results["hourly"][api_name]
                self._data[obj_name]["data"].extend(values)
            except KeyError:
                continue

    def _return_data(self, key: MeasType) -> Optional[tuple[list[dt.datetime], list[float]]]:
        """Useful help function for getting data from data
        dictionary without having to repeat code"""
        try:
            data_info = self._data[key]
            return data_info["time"], data_info["data"]
        except KeyError:
            return None
