# ================================================================
# FORECASTING SERVICE
# ================================================================

import numpy as np
import pandas as pd


# ================================================================
# MODEL FEATURES
# ================================================================

FEATURES = [
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
# MODEL TARGETS
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


LOOKBACK = 24


# ================================================================
# ADD HISTORICAL RAIN PROBABILITY
# ================================================================

def add_historical_rain_probability(
    weather_df,
    historical_rain_probability,
    pointid
):
    """
    Add historical rainfall probability to
    the API weather observations.

    Probability is obtained using:

        pointid + hour

    The probability table was calculated
    using training data only.
    """

    df = weather_df.copy()

    # ------------------------------------------------------------
    # Make sure datetime is datetime
    # ------------------------------------------------------------

    df["datetime"] = pd.to_datetime(
        df["datetime"]
    )

    # ------------------------------------------------------------
    # Extract hour
    # ------------------------------------------------------------

    df["hour"] = df["datetime"].dt.hour

    # ------------------------------------------------------------
    # Select probability records for this point
    # ------------------------------------------------------------

    probability = (
        historical_rain_probability[
            historical_rain_probability["pointid"]
            == pointid
        ][
            [
                "pointid",
                "hour",
                "historical_rain_probability"
            ]
        ]
        .copy()
    )

    # ------------------------------------------------------------
    # Merge using pointid + hour
    # ------------------------------------------------------------

    df = df.merge(
        probability,
        on=[
            "pointid",
            "hour"
        ],
        how="left"
    )

    # ------------------------------------------------------------
    # Check for missing probabilities
    # ------------------------------------------------------------

    if df[
        "historical_rain_probability"
    ].isna().any():

        raise ValueError(
            "Historical rainfall probability "
            "could not be found for some hours "
            "of the selected geographical point."
        )

    return df


# ================================================================
# PREPARE LSTM INPUT
# ================================================================

def prepare_lstm_input(
    weather_df,
    feature_scaler
):
    """
    Prepare the previous 24 hours for
    LSTM prediction.
    """

    df = weather_df.copy()

    # ------------------------------------------------------------
    # Check features
    # ------------------------------------------------------------

    missing_features = [
        feature
        for feature in FEATURES
        if feature not in df.columns
    ]

    if missing_features:

        raise ValueError(
            "Missing model features: "
            + ", ".join(
                missing_features
            )
        )

    # ------------------------------------------------------------
    # Sort chronologically
    # ------------------------------------------------------------

    df = df.sort_values(
        "datetime"
    ).reset_index(
        drop=True
    )

    # ------------------------------------------------------------
    # Get previous 24 hours
    # ------------------------------------------------------------

    sequence = df.tail(
        LOOKBACK
    )

    if len(sequence) < LOOKBACK:

        raise ValueError(
            f"Only {len(sequence)} "
            f"hourly observations available. "
            f"The model requires "
            f"{LOOKBACK} hours."
        )

    # ------------------------------------------------------------
    # Select exact feature order
    # ------------------------------------------------------------

    X = sequence[
        FEATURES
    ].copy()

    # ------------------------------------------------------------
    # Scale using training scaler
    # ------------------------------------------------------------

    X_scaled = feature_scaler.transform(
        X
    )

    # ------------------------------------------------------------
    # Convert to LSTM shape
    #
    # (1, 24, 10)
    # ------------------------------------------------------------

    X_scaled = np.asarray(
        X_scaled,
        dtype=np.float32
    )

    X_scaled = X_scaled.reshape(
        1,
        LOOKBACK,
        len(FEATURES)
    )

    return X_scaled, sequence


# ================================================================
# PREDICT NEXT HOUR
# ================================================================

def predict_next_hour(
    weather_df,
    model,
    feature_scaler,
    target_scaler
):
    """
    Predict the next hour using
    the previous 24 hours.
    """

    # ------------------------------------------------------------
    # Prepare sequence
    # ------------------------------------------------------------

    X, sequence = prepare_lstm_input(
        weather_df,
        feature_scaler
    )

    # ------------------------------------------------------------
    # LSTM prediction
    # ------------------------------------------------------------

    prediction_scaled = model.predict(
        X,
        verbose=0
    )

    # ------------------------------------------------------------
    # Convert prediction back to
    # original weather units
    # ------------------------------------------------------------

    prediction = target_scaler.inverse_transform(
        prediction_scaled
    )

    prediction = prediction[0]

    # ------------------------------------------------------------
    # Create prediction DataFrame
    # ------------------------------------------------------------

    prediction_df = pd.DataFrame(
        [
            prediction
        ],
        columns=TARGET_VARIABLES
    )

    return (
        prediction_df,
        sequence
    )