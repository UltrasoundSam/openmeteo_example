# OpenMeteo Python Wrapper

![Open-Meteo API](https://camo.githubusercontent.com/2d46b3ccedac13ebde59de388e9a4a7fc9a652fa4ee54e9f6e7a04eae4b3c7a9/68747470733a2f2f63646e2e737562737461636b2e636f6d2f696d6167652f66657463682f775f313336302c635f6c696d69742c665f6175746f2c715f6175746f3a626573742c666c5f70726f67726573736976653a73746565702f68747470732533412532462532466275636b65746565722d65303562626338342d626161332d343337652d393531382d6164623332626537373938342e73332e616d617a6f6e6177732e636f6d2532467075626c6963253246696d6167657325324666643064373935332d356139642d343431632d623539662d3463646532343435303361315f393334783436312e706e67)

![Tests](https://github.com/UltrasoundSam/openmeteo_example/actions/workflows/tests.yaml/badge.svg)

## Overview

The **OpenMeteo Python Wrapper** is a simple Python module that provides an interface to the [Open-Meteo API](https://open-meteo.com/en/docs/) for retrieving weather data. This wrapper simplifies API interactions by handling request formation, response parsing, and error handling, allowing users to fetch real-time and historical weather data with minimal effort.

## Features

- Fetch current weather data for any location (latitude & longitude)
- Retrieve weather forecasts for up to 7 days
- Access historical weather data
- Supports customization via optional query parameters
- No API key required (Open-Meteo API is free and open-access)

## Installation

Clone this repository and/or install:

```sh
# Clone the repository
git clone https://github.com/UltrasoundSam/openmeteo_example.git

# Install required dependencies
pip install git+https://github.com/UltrasoundSam/openmeteo_example.git
```

## Usage

### Different Classes

OpenMeteo_example has two primary classes that are used in this repository; ```MeteoHistorial``` and ```MeteoForecast``` to distinguish between historic datasets and forecasts.

### Example: Get Current Weather Data

```python
from openmeteo_example import MeteoForecast

# Define location as latitude and longitude
weather_location = (54.376640, -2.139470)

# Create MeteoForecast object
local_weather = MeteoForecast(latitude=weather_location[0],
                              longitude=weather_location[1])

print(local_weather.get_current_data['current'])
```

### Example: Get Historical Weather Data

```python
from openmeteo_example import MeteoHistorical
import datetime as dt

# Define location as latitude and longitude
weather_location = (48.648449, 11.668780)

# Create MeteoHistoric object (which automatically gets current data)
historic_weather = MeteoHistorical(latitude=weather_location[0],
                                   longitude=weather_location[1])

# Get data for all of February
date_start = dt.datetime(year=2025, month=2, day=1)
date_end = dt.datetime(year=2025, month=2, day=28, hour=23, minute=59)

historic_weather.get_data(start=date_start, end=date_start)

print(historic_weather.temperature)
```

<!-- Could be useful, but not ready yet
## API Endpoints Used
- `GET /v1/forecast?latitude={lat}&longitude={lon}&current_weather=true`
- `GET /v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max&timezone=auto`
- `GET /v1/history?latitude={lat}&longitude={lon}&start_date={start}&end_date={end}&temperature_unit=celsius` -->

## Licence

This project is licensed under the MIT Licence. See [`LICENCE`](./LICENCE) for more details.

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue to improve the module.

## Acknowledgements

This wrapper is built on top of the [Open-Meteo API](https://open-meteo.com/en/docs/) and is not affiliated with Open-Meteo.
