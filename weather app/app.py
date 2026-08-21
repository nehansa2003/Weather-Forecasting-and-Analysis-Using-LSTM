
import streamlit as st
import sys
import os


# ================================================================
# IMPORT PROJECT UTILITIES
# ================================================================

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from utils.styling import (
    apply_dashboard_style,
    show_hero,
    metric_card,
    feature_card,
    section_header,
    show_footer
)


# ================================================================
# PAGE CONFIG
# ================================================================

st.set_page_config(
    page_title="Sri Lanka Weather Dashboard",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ================================================================
# APPLY GLOBAL STYLE
# ================================================================

apply_dashboard_style()


# ================================================================
# SIDEBAR
# ================================================================

with st.sidebar:

    st.markdown("## 🌦️ Weather AI")

    st.caption("Analysis & Forecasting")

    st.divider()

    st.markdown("### 🧭 Navigation")

    st.info(
        """
        Use the pages below to explore
        historical weather patterns and
        Colombo weather forecasting.
        """
    )

    st.divider()

    st.markdown("### 📊 Dataset")

    st.write("2020 – 2025")

    st.markdown("### 📍 Study Area")

    st.write("5 Sri Lankan Districts")

    st.markdown("### 🤖 Model")

    st.write("LSTM")


# ================================================================
# HERO HEADER
# ================================================================

show_hero(
    "Sri Lanka Weather Analysis & Forecasting",
    "Interactive historical weather analysis and "
    "Colombo next-hour weather forecasting",
    "🌦️"
)


# ================================================================
# INTRODUCTION
# ================================================================

section_header(
    "Weather Intelligence Dashboard",
    "This application provides an interactive platform "
    "for exploring six years of hourly weather observations "
    "collected from five Sri Lankan districts. The system "
    "also provides an LSTM-based next-hour weather "
    "forecasting component for selected locations within "
    "the Colombo study area.",
    "🌍"
)


# ================================================================
# PROJECT OVERVIEW
# ================================================================

st.subheader("📌 Project Overview")

col1, col2, col3, col4 = st.columns(4)


with col1:

    metric_card(
        "📍",
        "5",
        "Districts"
    )


with col2:

    metric_card(
        "🗺️",
        "107",
        "Geographical Points"
    )


with col3:

    metric_card(
        "📅",
        "2020–2025",
        "Data Period"
    )


with col4:

    metric_card(
        "🤖",
        "LSTM",
        "Forecasting Model"
    )


# ================================================================
# DASHBOARD FEATURES
# ================================================================

section_header(
    "Dashboard Features",
    "Explore the major analysis and forecasting capabilities "
    "available in this application.",
    "✨"
)


# ================================================================
# FEATURE CARDS
# ================================================================

col1, col2, col3 = st.columns(
    3,
    gap="medium"
)


with col1:

    feature_card(
        "Historical Analysis",
        "Explore district-wise averages, hourly patterns, "
        "monthly patterns, seasonal patterns and yearly trends.",
        "📊"
    )


with col2:

    feature_card(
        "Rainfall Analysis",
        "Explore rainfall distributions, rainfall probability, "
        "rainfall heatmaps, spatial rainfall patterns and "
        "relationships between weather variables.",
        "🌧️"
    )


with col3:

    feature_card(
        "Weather Forecasting",
        "Enter a location within Colombo to find the nearest "
        "predefined weather point, retrieve the previous "
        "24 hours of weather observations and predict the "
        "next hour using the LSTM model.",
        "🤖"
    )


# ================================================================
# FORECASTING SYSTEM
# ================================================================

section_header(
    "How the Forecasting System Works",
    "The Colombo forecasting component follows the same "
    "historical-sequence approach used during LSTM model training.",
    "🔮"
)


# ================================================================
# FORECASTING PIPELINE
# ================================================================

col1, col2, col3, col4 = st.columns(
    4,
    gap="medium"
)


with col1:

    metric_card(
        "📍",
        "01",
        "Enter Location"
    )


with col2:

    metric_card(
        "🗺️",
        "02",
        "Find Nearest Point"
    )


with col3:

    metric_card(
        "🕐",
        "03",
        "Previous 24 Hours"
    )


with col4:

    metric_card(
        "🔮",
        "04",
        "Next-Hour Prediction"
    )


# ================================================================
# RESEARCH PROJECT
# ================================================================

section_header(
    "Research Project",
    "This dashboard was developed as part of a BSc (Hons) "
    "Data Science Capstone Project. The system combines "
    "historical weather analysis with deep-learning-based "
    "next-hour weather forecasting for Colombo district.",
    "🎓"
)


# ================================================================
# DATASET INFORMATION
# ================================================================

col1, col2 = st.columns(
    2,
    gap="medium"
)


with col1:

    feature_card(
        "Historical Weather Dataset",
        "Hourly weather observations covering the period "
        "from 2020 to 2025 across five Sri Lankan districts "
        "and 107 predefined geographical points.",
        "📚"
    )


with col2:

    feature_card(
        "Colombo LSTM Forecasting",
        "The forecasting model uses the previous 24 hours "
        "of weather observations to predict the next hour "
        "for a selected Colombo geographical point.",
        "🧠"
    )


# ================================================================
# FOOTER
# ================================================================

show_footer()
