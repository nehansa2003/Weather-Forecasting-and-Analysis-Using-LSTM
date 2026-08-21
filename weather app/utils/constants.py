# ================================================================
# APPLICATION CONSTANTS
# ================================================================

# ----------------------------------------------------------------
# Districts
# ----------------------------------------------------------------

DISTRICTS = [
    "Colombo",
    "Galle",
    "Gampaha",
    "Jaffna",
    "Kandy"
]


# ----------------------------------------------------------------
# Main weather variables used in analysis
# ----------------------------------------------------------------

WEATHER_VARIABLES = [
    "temperature_c",
    "feelslike_c",
    "humidity_pct",
    "dewpoint_c",
    "pressure_hpa",
    "windspeed_kmh",
    "windgust_kmh",
    "rainfall_mm",
    "cloudcover_pct",
    "solarradiation_wm2",
    "sunshineduration_s"
]


# ----------------------------------------------------------------
# Variables used for district average
# ----------------------------------------------------------------

DISTRICT_AVERAGE_VARIABLES = [
    "temperature_c",
    "humidity_pct",
    "pressure_hpa",
    "windspeed_kmh",
    "windgust_kmh",
    "rainfall_mm",
    "cloudcover_pct",
    "solarradiation_wm2",
    "sunshineduration_s"
]


# ----------------------------------------------------------------
# Variables used in hourly analysis
# ----------------------------------------------------------------

HOURLY_VARIABLES = [
    "temperature_c",
    "humidity_pct",
    "pressure_hpa",
    "windspeed_kmh",
    "rainfall_mm",
    "windgust_kmh",
    "cloudcover_pct"
]


# ----------------------------------------------------------------
# Variables used in yearly analysis
# ----------------------------------------------------------------

YEARLY_VARIABLES = [
    "temperature_c",
    "humidity_pct",
    "pressure_hpa",
    "windspeed_kmh",
    "rainfall_mm",
    "cloudcover_pct",
    "windgust_kmh"
]


# ----------------------------------------------------------------
# Variables used in seasonal analysis
# ----------------------------------------------------------------

SEASONAL_VARIABLES = [
    "temperature_c",
    "humidity_pct",
    "pressure_hpa",
    "windspeed_kmh",
    "rainfall_mm",
    "windgust_kmh",
    "cloudcover_pct"
]


# ----------------------------------------------------------------
# Variables used in monthly analysis
# ----------------------------------------------------------------

MONTHLY_VARIABLES = [
    "temperature_c",
    "humidity_pct",
    "pressure_hpa",
    "windspeed_kmh",
    "rainfall_mm",
    "windgust_kmh",
    "cloudcover_pct"
]


# ----------------------------------------------------------------
# Correlation variables
# ----------------------------------------------------------------

CORRELATION_VARIABLES = [
    "temperature_c",
    "humidity_pct",
    "pressure_hpa",
    "windspeed_kmh",
    "rainfall_mm",
    "cloudcover_pct",
    "solarradiation_wm2",
    "feelslike_c",
    "dewpoint_c",
    "winddirection_deg",
    "windgust_kmh",
    "sunshineduration_s"
]


# ----------------------------------------------------------------
# Linear relationship pairs
# ----------------------------------------------------------------

RELATIONSHIP_PAIRS = [
    ("temperature_c", "humidity_pct"),
    ("temperature_c", "dewpoint_c"),
    ("humidity_pct", "rainfall_mm"),
    ("cloudcover_pct", "rainfall_mm"),
    ("pressure_hpa", "rainfall_mm"),
    ("windspeed_kmh", "rainfall_mm")
]


# ----------------------------------------------------------------
# Labels
# ----------------------------------------------------------------

VARIABLE_LABELS = {
    "temperature_c": ("Temperature", "Temperature (°C)"),
    "feelslike_c": ("Feels Like", "Feels Like (°C)"),
    "humidity_pct": ("Humidity", "Humidity (%)"),
    "dewpoint_c": ("Dew Point", "Dew Point (°C)"),
    "pressure_hpa": ("Atmospheric Pressure", "Pressure (hPa)"),
    "windspeed_kmh": ("Wind Speed", "Wind Speed (km/h)"),
    "windgust_kmh": ("Wind Gust", "Wind Gust (km/h)"),
    "rainfall_mm": ("Rainfall", "Rainfall (mm)"),
    "cloudcover_pct": ("Cloud Cover", "Cloud Cover (%)"),
    "solarradiation_wm2": (
        "Solar Radiation",
        "Solar Radiation (W/m²)"
    ),
    "sunshineduration_s": (
        "Sunshine Duration",
        "Sunshine Duration (s)"
    ),
    "winddirection_deg": (
        "Wind Direction",
        "Wind Direction (degrees)"
    )
}


# ----------------------------------------------------------------
# Rain threshold
# ----------------------------------------------------------------

RAIN_THRESHOLD = 0.1


# ----------------------------------------------------------------
# Dataset path
# ----------------------------------------------------------------

DATA_PATH = "data/weather_data_processed_2020_2025.parquet"

import os


# ================================================================
# PROJECT ROOT
# ================================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# ================================================================
# DATA
# ================================================================

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "weather_data_processed_2020_2025.parquet"
)

HISTORICAL_RAIN_PROBABILITY_PATH = os.path.join(
    BASE_DIR,
    "data",
    "historical_rain_probability.parquet"
)


# ================================================================
# MODEL
# ================================================================

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "lstm_weather_forecasting.keras"
)


# ================================================================
# SCALERS
# ================================================================

FEATURE_SCALER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "feature_standard_scaler.pkl"
)

TARGET_SCALER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "target_standard_scaler.pkl"
)


# ================================================================
# LSTM CONFIGURATION
# ================================================================

LOOKBACK = 24


# ================================================================
# MODEL FEATURES
# ================================================================

MODEL_FEATURES = [
    "temperature_c",
    "humidity_pct",
    "pressure_hpa",
    "windspeed_kmh",
    "rainfall_mm",
    "windgust_kmh",
    "cloudcover_pct",
    "solarradiation_wm2",
    "dewpoint_c",
    "historical_rain_probability"
]


# ================================================================
# TARGET VARIABLES
# ================================================================

TARGET_VARIABLES = [
    "temperature_c",
    "humidity_pct",
    "pressure_hpa",
    "windspeed_kmh",
    "rainfall_mm",
    "windgust_kmh",
    "cloudcover_pct",
    "solarradiation_wm2",
    "dewpoint_c"
]

