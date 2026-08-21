# ================================================================
# GEOCODING SERVICE
# ================================================================

import requests


def geocode_location(
    location_name
):
    """
    Convert a location name into:
        - area name
        - latitude
        - longitude
    """

    url = (
        "https://geocoding-api.open-meteo.com/v1/search"
    )

    params = {

        "name": location_name,

        "count": 1,

        "language": "en",

        "format": "json"
    }

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    results = data.get(
        "results",
        []
    )

    if not results:

        return None

    result = results[0]

    return {
        "name": result.get(
            "name",
            location_name
        ),

        "latitude": result.get(
            "latitude"
        ),

        "longitude": result.get(
            "longitude"
        ),

        "country": result.get(
            "country",
            ""
        ),

        "admin1": result.get(
            "admin1",
            ""
        )
    }