import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from utils.constants import DATA_PATH
from utils.styling import (
    apply_dashboard_style,
    show_hero,
    metric_card,
    info_card,
    show_footer
)

# ================================================================
# CONFIG
# ================================================================

st.set_page_config(
    page_title="Dataset Overview",
    page_icon="📊",
    layout="wide"
)

apply_dashboard_style()


# ================================================================
# LOAD DATA
# ================================================================

@st.cache_data
def load_data():

    df = pd.read_parquet(
        DATA_PATH,
        engine="pyarrow"
    )

    df["datetime"] = pd.to_datetime(
        df["datetime"]
    )

    return df


weather_df = load_data()


# ================================================================
# HERO
# ================================================================

show_hero(
    "Dataset Overview",
    "Explore the structure and coverage of the historical weather dataset",
    "📊"
)


# ================================================================
# METRICS
# ================================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card(
        "📚",
        f"{len(weather_df):,}",
        "Weather Records"
    )

with col2:
    metric_card(
        "📋",
        weather_df.shape[1],
        "Variables"
    )

with col3:
    metric_card(
        "🏙️",
        weather_df["district"].nunique(),
        "Districts"
    )

with col4:
    metric_card(
        "📍",
        weather_df[
            "global_pointid"
        ].nunique(),
        "Geographical Points"
    )


st.markdown("<br>", unsafe_allow_html=True)


# ================================================================
# DATA PERIOD
# ================================================================
st.subheader("📅 Data Coverage")

col1, col2 = st.columns(2)

with col1:

    info_card(
        "Start",
        weather_df["datetime"]
        .min()
        .strftime("%d %B %Y %H:%M"),
        "🟢"
    )

with col2:

    info_card(
        "End",
        weather_df["datetime"]
        .max()
        .strftime("%d %B %Y %H:%M"),
        "🔵"
    )

# ================================================================
# DISTRICTS
# ================================================================

st.subheader(
    "📍 Study Districts"
)

districts = sorted(
    weather_df["district"].unique()
)

cols = st.columns(
    len(districts)
)

district_icons = [
    "🏙️",
    "🌴",
    "🌿",
    "🌾",
    "⛰️"
]

for i, district in enumerate(districts):

    with cols[i]:

        metric_card(
            district_icons[i],
            district,
            "Study District"
        )


# ================================================================
# VARIABLES
# ================================================================

st.subheader(
    "🌡️ Weather Variables"
)

weather_columns = [
    "temperature_c",
    "feelslike_c",
    "humidity_pct",
    "dewpoint_c",
    "pressure_hpa",
    "windspeed_kmh",
    "winddirection_deg",
    "windgust_kmh",
    "rainfall_mm",
    "cloudcover_pct",
    "solarradiation_wm2",
    "sunshineduration_s"
]

available = [
    x for x in weather_columns
    if x in weather_df.columns
]

variable_df = pd.DataFrame(
    {
        "Weather Variable": available
    }
)

st.dataframe(
    variable_df,
    use_container_width=True,
    hide_index=True
)


# ================================================================
# SAMPLE DATA
# ================================================================

with st.expander(
    "🔍 Preview Dataset"
):

    st.dataframe(
        weather_df.head(20),
        use_container_width=True,
        hide_index=True
    )


show_footer()