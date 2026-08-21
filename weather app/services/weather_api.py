# ================================================================
# WEATHER API SERVICE
# ================================================================

import requests
import pandas as pd


def get_recent_weather(
    latitude,
    longitude,
    past_days=2
):
    """
    Retrieve recent hourly weather data.

    Two days are requested to ensure that at least
    the previous 24 completed hourly observations
    are available.
    """

    url = (
        "https://api.open-meteo.com/v1/forecast"
    )

    params = {
        "latitude": latitude,
        "longitude": longitude,

        "past_days": past_days,

        "hourly": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "dew_point_2m,"
            "pressure_msl,"
            "wind_speed_10m,"
            "wind_gusts_10m,"
            "precipitation,"
            "cloud_cover,"
            "shortwave_radiation"
        ),

        "timezone": "Asia/Colombo"
    }

    response = requests.get(
        url,
        params=params,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    return convert_api_to_dataframe(
        data
    )


# ================================================================
# CONVERT API RESPONSE
# ================================================================

def convert_api_to_dataframe(
    api_data
):
    """
    Convert Open-Meteo hourly response
    to the exact weather column names
    used by the LSTM model.
    """

    hourly = api_data["hourly"]

    df = pd.DataFrame(
        {
            "datetime": pd.to_datetime(
                hourly["time"]
            ),

            "temperature_c":
                hourly["temperature_2m"],

            "humidity_pct":
                hourly["relative_humidity_2m"],

            "dewpoint_c":
                hourly["dew_point_2m"],

            "pressure_hpa":
                hourly["pressure_msl"],

            "windspeed_kmh":
                hourly["wind_speed_10m"],

            "windgust_kmh":
                hourly["wind_gusts_10m"],

            "rainfall_mm":
                hourly["precipitation"],

            "cloudcover_pct":
                hourly["cloud_cover"],

            "solarradiation_wm2":
                hourly["shortwave_radiation"]
        }
    )

    return df