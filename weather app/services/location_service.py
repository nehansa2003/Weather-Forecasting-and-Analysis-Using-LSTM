# ================================================================
# LOCATION SERVICE
# ================================================================

import numpy as np


def haversine_distance(
    latitude1,
    longitude1,
    latitude2,
    longitude2
):
    """
    Calculate distance between geographical
    coordinates using the Haversine formula.

    Returns distance in kilometres.
    """

    earth_radius = 6371.0

    lat1 = np.radians(latitude1)
    lat2 = np.radians(latitude2)

    delta_lat = np.radians(
        latitude2 - latitude1
    )

    delta_lon = np.radians(
        longitude2 - longitude1
    )

    a = (
        np.sin(delta_lat / 2) ** 2
        +
        np.cos(lat1)
        * np.cos(lat2)
        * np.sin(delta_lon / 2) ** 2
    )

    c = 2 * np.arcsin(
        np.sqrt(a)
    )

    return earth_radius * c


def find_nearest_colombo_point(
    latitude,
    longitude,
    weather_df
):
    """
    Find the geographical point closest
    to the supplied location.
    """

    colombo_points = (
        weather_df[
            weather_df["district"]
            .str.lower()
            == "colombo"
        ][
            [
                "pointid",
                "global_pointid",
                "latitude",
                "longitude",
                "elevation_m"
            ]
        ]
        .drop_duplicates(
            subset=["pointid"]
        )
        .copy()
    )

    colombo_points[
        "distance_km"
    ] = haversine_distance(
        latitude,
        longitude,
        colombo_points["latitude"].values,
        colombo_points["longitude"].values
    )

    nearest_point = (
        colombo_points
        .sort_values("distance_km")
        .iloc[0]
    )

    return nearest_point