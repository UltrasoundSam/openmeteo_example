# -*- coding: utf-8 -*-
"""
Created on Tues November 25 2025 11:25

@author: samhill

This file creates the MeteoHistorical class that encapsulates everything to do
with historic data from OpenMeteo
"""

import datetime as dt
from typing import Optional
from .openmeteo import OpenMeteo


class MeteoHistorical(OpenMeteo):
    # Point to Historic/archive endpoint
    base_url = "https://archive-api.open-meteo.com/v1/archive"

    def get_data(
        self,
        start_date: Optional[dt.datetime] = None,
        end_date: Optional[dt.datetime] = None,
        temperature: bool = True,
        wind_speed: bool = True,
        cloud_cover: bool = True,
        precipitation: bool = True,
    ):
        """Refine get data method for historical data"""
        if start_date is None:
            start_date = dt.datetime.now() - dt.timedelta(days=14)
        if end_date is None:
            end_date = dt.datetime.now() - -dt.timedelta(days=7)

        super().get_data(
            start_date=start_date,
            end_date=end_date,
            temperature=temperature,
            wind_speed=wind_speed,
            cloud_cover=cloud_cover,
            precipitation=precipitation,
        )
