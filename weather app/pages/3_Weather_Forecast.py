# ================================================================
# IMPORT LIBRARIES
# ================================================================

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import tensorflow as tf
import requests
from urllib.parse import urlparse, parse_qs
import sys
import os


# ================================================================
# PROJECT PATH
# ================================================================

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


# ================================================================
# IMPORT PROJECT FILES
# ================================================================

from utils.constants import (
    DATA_PATH,
    MODEL_PATH,
    FEATURE_SCALER_PATH,
    TARGET_SCALER_PATH,
    HISTORICAL_RAIN_PROBABILITY_PATH
)

from utils.styling import (
    apply_dashboard_style,
    show_hero,
    metric_card,
    section_header,
    show_footer
)

from services.location_service import (
    find_nearest_colombo_point
)

from services.weather_api import (
    get_recent_weather
)

from services.forecasting_service import (
    add_historical_rain_probability,
    predict_next_hour,
    TARGET_VARIABLES
)


# ================================================================
# PAGE CONFIG
# ================================================================

st.set_page_config(
    page_title="Weather Forecast",
    page_icon="🔮",
    layout="wide"
)


# ================================================================
# APPLY STYLE
# ================================================================

apply_dashboard_style()


# ================================================================
# LOAD MODEL
# ================================================================

@st.cache_resource
def load_model_and_scalers():

    model = tf.keras.models.load_model(
        MODEL_PATH
    )

    feature_scaler = joblib.load(
        FEATURE_SCALER_PATH
    )

    target_scaler = joblib.load(
        TARGET_SCALER_PATH
    )

    return (
        model,
        feature_scaler,
        target_scaler
    )


# ================================================================
# LOAD GEOGRAPHICAL POINTS
# ================================================================

@st.cache_data
def load_weather_points():

    df = pd.read_parquet(
        DATA_PATH,
        columns=[
            "district",
            "pointid",
            "global_pointid",
            "latitude",
            "longitude",
            "elevation_m"
        ]
    )

    return df.drop_duplicates(
        subset=[
            "global_pointid"
        ]
    )


# ================================================================
# LOAD HISTORICAL RAIN PROBABILITY
# ================================================================

@st.cache_data
def load_rain_probability():

    df = pd.read_parquet(
        HISTORICAL_RAIN_PROBABILITY_PATH
    )

    return df


# ================================================================
# LOAD RESOURCES
# ================================================================

weather_points = load_weather_points()

historical_rain_probability = (
    load_rain_probability()
)

model, feature_scaler, target_scaler = (
    load_model_and_scalers()
)


# ================================================================
# HERO
# ================================================================

show_hero(
    "Colombo Next-Hour Weather Forecast",
    "Enter a location to identify the nearest geographical point and predict the next hour using the previous 24 hours of weather observations.",
    "🔮"
)


# ================================================================
# LOCATION INPUT
# ================================================================

section_header(
    "Select Forecast Location",
    "Enter a Google Maps location link or coordinates within the Colombo study area.",
    "📍"
)


location_input = st.text_input(
    "🔗 Google Maps Link or Location",
    placeholder=(
        "Paste a Google Maps link here..."
    )
)


# ================================================================
# COORDINATE INPUT
# ================================================================

st.caption(
    "Alternatively, manually enter latitude and longitude."
)

col1, col2 = st.columns(2)

with col1:

    latitude_input = st.number_input(
        "Latitude",
        min_value=5.0,
        max_value=10.0,
        value=6.9271,
        format="%.5f"
    )


with col2:

    longitude_input = st.number_input(
        "Longitude",
        min_value=78.0,
        max_value=82.0,
        value=79.8612,
        format="%.5f"
    )


# ================================================================
# EXTRACT COORDINATES FROM LINK
# ================================================================

def extract_coordinates_from_link(
    link
):
    """
    Attempt to extract latitude and longitude
    from a Google Maps URL.
    """

    if not link:

        return None, None

    try:

        # --------------------------------------------------------
        # @latitude,longitude
        # --------------------------------------------------------

        if "@" in link:

            coordinates = (
                link
                .split("@")[1]
                .split(",")
            )

            latitude = float(
                coordinates[0]
            )

            longitude = float(
                coordinates[1]
            )

            return (
                latitude,
                longitude
            )


        # --------------------------------------------------------
        # query parameters
        # --------------------------------------------------------

        parsed_url = urlparse(
            link
        )

        query = parse_qs(
            parsed_url.query
        )

        if "q" in query:

            coordinates = (
                query["q"][0]
                .split(",")
            )

            latitude = float(
                coordinates[0]
            )

            longitude = float(
                coordinates[1]
            )

            return (
                latitude,
                longitude
            )

    except Exception:

        return None, None

    return None, None


# ================================================================
# REVERSE GEOCODING
# ================================================================

def get_location_name(
    latitude,
    longitude
):
    """
    Retrieve approximate area name using
    OpenStreetMap Nominatim.
    """

    try:

        url = (
            "https://nominatim.openstreetmap.org/reverse"
        )

        params = {
            "lat": latitude,
            "lon": longitude,
            "format": "json"
        }

        headers = {
            "User-Agent":
            "SriLankaWeatherForecastApp"
        }

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "display_name",
            "Unknown Location"
        )

    except Exception:

        return (
            "Location name unavailable"
        )


# ================================================================
# PREDICT BUTTON
# ================================================================

predict_button = st.button(
    "🔮 Predict Next-Hour Weather",
    type="primary",
    use_container_width=True
)



# ================================================================
# FORECAST PIPELINE
# ================================================================

if predict_button:

    try:

        # ========================================================
        # GET LOCATION
        # ========================================================

        latitude = latitude_input
        longitude = longitude_input


        # If link entered, try to use coordinates from link

        if location_input:

            link_latitude, link_longitude = (
                extract_coordinates_from_link(
                    location_input
                )
            )

            if (
                link_latitude is not None
                and link_longitude is not None
            ):

                latitude = link_latitude
                longitude = link_longitude

                st.success(
                    "Location coordinates extracted successfully."
                )

            else:

                st.warning(
                    "Coordinates could not be extracted "
                    "from the link. Manual coordinates "
                    "will be used."
                )


        # ========================================================
        # GET LOCATION NAME
        # ========================================================

        location_name = get_location_name(
            latitude,
            longitude
        )


        # ========================================================
        # FIND NEAREST POINT
        # ========================================================

        nearest_point = (
            find_nearest_colombo_point(
                latitude,
                longitude,
                weather_points
            )
        )


        nearest_latitude = float(
            nearest_point["latitude"]
        )

        nearest_longitude = float(
            nearest_point["longitude"]
        )

        nearest_pointid = int(
            nearest_point["pointid"]
        )

        distance_km = float(
            nearest_point["distance_km"]
        )


        # ========================================================
        # DISPLAY LOCATION INFORMATION
        # ========================================================

        section_header(
            "Selected Location",
            "The nearest predefined Colombo geographical point will be used for weather retrieval and forecasting.",
            "📍"
        )


        col1, col2, col3, col4 = (
            st.columns(4)
        )


        with col1:

            metric_card(
                "📌",
                nearest_pointid,
                "Nearest Point ID"
            )


        with col2:

            metric_card(
                "📏",
                f"{distance_km:.2f} km",
                "Distance"
            )


        with col3:

            metric_card(
                "🌐",
                f"{nearest_latitude:.4f}",
                "Latitude"
            )


        with col4:

            metric_card(
                "🌐",
                f"{nearest_longitude:.4f}",
                "Longitude"
            )


        st.info(
            f"📍 Approximate location: {location_name}"
        )


        # ========================================================
        # GET RECENT WEATHER
        # ========================================================

        with st.spinner(
            "Retrieving recent weather observations..."
        ):

            recent_weather = (
                get_recent_weather(
                    nearest_latitude,
                    nearest_longitude,
                    past_days=2
                )
            )


        # ========================================================
        # ADD POINT INFORMATION
        # ========================================================

        recent_weather[
            "pointid"
        ] = nearest_pointid


        recent_weather[
            "district"
        ] = "Colombo"


        # ========================================================
        # REMOVE FUTURE HOURS
        # ========================================================

        current_time = (
            pd.Timestamp.now(
                tz="Asia/Colombo"
            )
            .tz_localize(None)
        )


        recent_weather = (
            recent_weather[
                recent_weather["datetime"]
                <= current_time
            ]
            .copy()
        )


        # ========================================================
        # KEEP PREVIOUS 24 HOURS
        # ========================================================

        recent_weather = (
            recent_weather
            .sort_values(
                "datetime"
            )
            .tail(24)
            .copy()
        )


        # ========================================================
        # CHECK DATA
        # ========================================================

        if len(recent_weather) < 24:

            raise ValueError(
                "Unable to retrieve a complete "
                "24-hour weather sequence."
            )


        # ========================================================
        # ADD HISTORICAL RAIN PROBABILITY
        # ========================================================

        recent_weather = (
            add_historical_rain_probability(
                recent_weather,
                historical_rain_probability,
                nearest_pointid
            )
        )


        # ========================================================
        # PREDICT
        # ========================================================

        with st.spinner(
            "Running LSTM next-hour prediction..."
        ):

            prediction_df, sequence = (
                predict_next_hour(
                    recent_weather,
                    model,
                    feature_scaler,
                    target_scaler
                )
            )


        # ========================================================
        # CLEAN PREDICTIONS
        # ========================================================

        prediction_df[
            "rainfall_mm"
        ] = np.maximum(
            prediction_df[
                "rainfall_mm"
            ],
            0
        )


        prediction_df[
            "cloudcover_pct"
        ] = np.clip(
            prediction_df[
                "cloudcover_pct"
            ],
            0,
            100
        )


        prediction_df[
            "humidity_pct"
        ] = np.clip(
            prediction_df[
                "humidity_pct"
            ],
            0,
            100
        )


        # ========================================================
        # PREDICTED TIME
        # ========================================================

        latest_time = (
            sequence[
                "datetime"
            ].max()
        )

        prediction_time = (
            latest_time
            + pd.Timedelta(hours=1)
        )


        # ========================================================
        # CURRENT WEATHER
        # ========================================================

        section_header(
            "Current Weather",
            f"Latest weather observation: {latest_time.strftime('%d %B %Y %H:%M')}",
            "🌤️"
        )


        current_weather = (
            sequence
            .iloc[-1]
        )


        col1, col2, col3, col4 = (
            st.columns(4)
        )


        with col1:

            metric_card(
                "🌡️",
                f"{current_weather['temperature_c']:.1f} °C",
                "Temperature"
            )


        with col2:

            metric_card(
                "💧",
                f"{current_weather['humidity_pct']:.1f} %",
                "Humidity"
            )


        with col3:

            metric_card(
                "🌧️",
                f"{current_weather['rainfall_mm']:.1f} mm",
                "Rainfall"
            )


        with col4:

            metric_card(
                "💨",
                f"{current_weather['windspeed_kmh']:.1f} km/h",
                "Wind Speed"
            )


        # ========================================================
        # PREDICTED WEATHER
        # ========================================================

        section_header(
            "Next-Hour Weather Prediction",
            f"Forecast for {prediction_time.strftime('%d %B %Y at %H:%M')}",
            "🔮"
        )


        col1, col2, col3, col4 = (
            st.columns(4)
        )


        with col1:

            metric_card(
                "🌡️",
                f"{prediction_df.iloc[0]['temperature_c']:.1f} °C",
                "Predicted Temperature"
            )


        with col2:

            metric_card(
                "💧",
                f"{prediction_df.iloc[0]['humidity_pct']:.1f} %",
                "Predicted Humidity"
            )


        with col3:

            metric_card(
                "🌧️",
                f"{prediction_df.iloc[0]['rainfall_mm']:.2f} mm",
                "Predicted Rainfall"
            )


        with col4:

            metric_card(
                "💨",
                f"{prediction_df.iloc[0]['windspeed_kmh']:.1f} km/h",
                "Predicted Wind Speed"
            )


        # ========================================================
        # COMPLETE FORECAST TABLE
        # ========================================================

        section_header(
            "Complete Weather Forecast",
            "Predicted values for all nine weather variables.",
            "📊"
        )


        forecast_display = (
            prediction_df
            .T
            .reset_index()
        )

        forecast_display.columns = [
            "Weather Variable",
            "Predicted Value"
        ]


        forecast_display[
            "Predicted Value"
        ] = forecast_display[
            "Predicted Value"
        ].round(3)


        st.dataframe(
            forecast_display,
            use_container_width=True,
            hide_index=True
        )


        # ========================================================
        # CURRENT VS PREDICTED
        # ========================================================

        section_header(
            "Current vs Next Hour",
            "Compare the latest weather observation with the LSTM forecast.",
            "📈"
        )


        comparison = pd.DataFrame(
            {
                "Current": [
                    current_weather[
                        variable
                    ]
                    for variable
                    in TARGET_VARIABLES
                ],

                "Predicted": [
                    prediction_df.iloc[0][
                        variable
                    ]
                    for variable
                    in TARGET_VARIABLES
                ]
            },

            index=TARGET_VARIABLES
        )


        st.bar_chart(
            comparison
        )


        # ========================================================
        # LAST 24 HOURS
        # ========================================================

        section_header(
            "Previous 24-Hour Weather Pattern",
            "Weather observations used as input to the LSTM model.",
            "📉"
        )


        chart_data = (
            sequence[
                [
                    "datetime",
                    "temperature_c",
                    "humidity_pct",
                    "windspeed_kmh"
                ]
            ]
            .set_index(
                "datetime"
            )
        )


        st.line_chart(
            chart_data
        )


        # ========================================================
        # SUCCESS
        # ========================================================

        st.success(
            "Next-hour weather prediction completed successfully!"
        )


    except Exception as error:

        st.error(
            f"Forecasting error: {error}"
        )
# ================================================================
# PAGE FOOTER
# ================================================================
show_footer()