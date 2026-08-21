import streamlit as st
import os
import sys
import pandas as pd


# ================================================================
# PATH SETUP
# ================================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(BASE_DIR)


from utils.styling import (
    apply_dashboard_style,
    show_hero,
    metric_card,
    section_header,
    info_card,
    show_footer
)


# ================================================================
# PAGE CONFIG
# ================================================================

st.set_page_config(
    page_title="LSTM Model Results",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ================================================================
# APPLY STYLE
# ================================================================

apply_dashboard_style()


# ================================================================
# ASSETS PATH
# ================================================================

ASSETS_DIR = os.path.join(
    BASE_DIR,
    "assets"
)


# ================================================================
# HELPER FUNCTIONS
# ================================================================

def asset_path(filename):

    return os.path.join(
        ASSETS_DIR,
        filename
    )


def show_chart(
    filename,
    caption=None,
    width=None
):

    path = asset_path(filename)

    if os.path.exists(path):

        st.image(
            path,
            use_container_width=True
        )

        if caption:

            st.caption(caption)

    else:

        st.warning(
            f"Chart not found: {filename}"
        )


# ================================================================
# SIDEBAR
# ================================================================

with st.sidebar:

    st.markdown(
        """
        # 🤖 LSTM Model
        """
    )

    st.caption(
        "Training & Evaluation"
    )

    st.divider()

    st.markdown("### 🧭 Navigation")

    st.info(
        "Explore the LSTM model architecture, "
        "training process, evaluation results, "
        "and prediction performance."
    )

    st.divider()

    st.markdown("### 📊 Model Information")

    st.markdown(
        """
        **📍 Study Area**  
        Colombo District

        **⏱️ Lookback**  
        24 hours

        **🔮 Forecast Horizon**  
        1 hour

        **🤖 Model**  
        LSTM

        **🎯 Outputs**  
        9 Weather Variables
        """
    )
    st.divider()

    # st.markdown(
    #     """
    #     ### 🧭 Model Results

    #     Explore:

    #     • Dataset configuration  
    #     • Training configuration  
    #     • Training performance  
    #     • Test evaluation  
    #     • Prediction results  
    #     • Rain / No-Rain performance
    #     """
    # )

    # st.divider()

    # st.markdown(
    #     """
    #     **📍 District**

    #     Colombo

    #     **⏱️ Forecast Horizon**

    #     1 Hour

    #     **🧠 Model**

    #     LSTM

    #     **📚 Lookback**

    #     24 Hours
    #     """
    # )


# ================================================================
# HERO
# ================================================================

show_hero(
    "Colombo LSTM Weather Forecasting Model",
    "Model architecture, training process, evaluation results and prediction performance",
    "🤖"
)


# ================================================================
# MODEL OVERVIEW
# ================================================================

section_header(
    "Model Overview",
    "Summary of the Colombo district LSTM forecasting experiment."
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    metric_card(
        "📍",
        "Colombo",
        "Study District"
    )


with col2:

    metric_card(
        "⏱️",
        "24 Hours",
        "Lookback Window"
    )


with col3:

    metric_card(
        "🔮",
        "1 Hour",
        "Forecast Horizon"
    )


with col4:

    metric_card(
        "🎯",
        "9",
        "Prediction Targets"
    )


# ================================================================
# DATASET DETAILS
# ================================================================

section_header(
    "Model Dataset",
    "The LSTM model was trained using hourly observations from the Colombo district.",
    "📊"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    metric_card(
        "📚",
        "578,688",
        "Total Records"
    )


with col2:

    metric_card(
        "📅",
        "2020–2025",
        "Data Period"
    )


with col3:

    metric_card(
        "📍",
        "11",
        "Geographical Points"
    )


with col4:

    metric_card(
        "🕐",
        "Hourly",
        "Observation Frequency"
    )


st.markdown("<br>", unsafe_allow_html=True)


dataset_info = pd.DataFrame(
    {
        "Dataset Component": [
            "Total observations",
            "Training observations",
            "Validation observations",
            "Testing observations",
            "Training period",
            "Validation period",
            "Testing period",
            "Lookback",
            "Forecast horizon"
        ],

        "Value": [
            "578,688",
            "385,704",
            "96,624",
            "96,360",
            "2020–2023",
            "2024",
            "2025",
            "24 hours",
            "1 hour"
        ]
    }
)


st.dataframe(
    dataset_info,
    width=750,
    height=352,
    #use_container_width=True,
    hide_index=True
)


# ================================================================
# DATA SPLIT
# ================================================================

section_header(
    "Training, Validation and Testing Split",
    "The dataset was divided chronologically to preserve the temporal nature of the weather forecasting problem."
)


col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        """
        <div class="info-card">

        <b>🟢 Training Dataset</b>

        <br>

        <b>Period:</b> 2020–2023

        <br>

        <b>Records:</b> 385,704

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        """
        <div class="info-card">

        <b>🔵 Validation Dataset</b>

        <br>

        <b>Period:</b> 2024

        <br>

        <b>Records:</b> 96,624

        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        """
        <div class="info-card">

        <b>🟣 Testing Dataset</b>

        <br>

        <b>Period:</b> 2025

        <br>

        <b>Records:</b> 96,360

        </div>
        """,
        unsafe_allow_html=True
    )


# ================================================================
# MODEL FEATURES
# ================================================================

section_header(
    "Model Input Features",
    "The LSTM receives the previous 24 hours of observations for the following ten input features.",
    "📥"
)


feature_list = [
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


feature_df = pd.DataFrame(
    {
        "No.": range(1, len(feature_list) + 1),
        "Input Feature": feature_list
    }
)


st.dataframe(
    feature_df,
    width=550,
    height=388,
    #use_container_width=True,
    hide_index=True
)


# ================================================================
# TARGET VARIABLES
# ================================================================

section_header(
    "Prediction Target Variables",
    "The trained LSTM simultaneously predicts nine weather variables for the next hour.",
    "🎯"
)


target_list = [
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


target_df = pd.DataFrame(
    {
        "No.": range(1, len(target_list) + 1),
        "Target Variable": target_list
    }
)


st.dataframe(
    target_df,
    width=550,
    height=352,
    #use_container_width=True,
    hide_index=True
)


# ================================================================
# PREPROCESSING
# ================================================================

section_header(
    "Data Preprocessing",
    "StandardScaler was fitted using training data only and then applied to the training, validation and testing datasets.",
    "⚙️"
)


col1, col2 = st.columns(2)


with col1:

    st.markdown(
        """
        <div class="section-card">

        ### 📥 Input Scaling

        <p>
        The ten input features were standardized using
        the training dataset's mean and standard deviation.
        </p>

        <b>Scaler:</b> StandardScaler

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        """
        <div class="section-card">

        ### 🎯 Target Scaling

        <p>
        The nine prediction targets were standardized
        using a separate StandardScaler fitted only
        on the training data.
        </p>

        <b>Scaler:</b> StandardScaler

        </div>
        """,
        unsafe_allow_html=True
    )


# ================================================================
# SEQUENCE DETAILS
# ================================================================

section_header(
    "Sequence Generation",
    "Each prediction uses the previous 24 hourly observations to forecast the following hour.",
    "🔄"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    metric_card(
        "🕐",
        "24",
        "Input Time Steps"
    )


with col2:

    metric_card(
        "🔮",
        "1",
        "Future Time Step"
    )


with col3:

    metric_card(
        "📈",
        "385,440",
        "Training Sequences"
    )


with col4:

    metric_card(
        "🧪",
        "96,360",
        "Validation Sequences"
    )


# ================================================================
# MODEL ARCHITECTURE
# ================================================================

section_header(
    "LSTM Model Architecture",
    "The forecasting model uses a stacked LSTM architecture followed by dense layers for multi-output regression."
)


architecture_df = pd.DataFrame(
    {
        "Layer": [
            "LSTM",
            "Dropout",
            "LSTM",
            "Dropout",
            "Dense",
            "Output Dense"
        ],

        "Configuration": [
            "64 units, return_sequences=True",
            "0.20",
            "32 units",
            "0.20",
            "32 units, ReLU",
            "9 outputs, Linear"
        ]
    }
)


st.dataframe(
    architecture_df,
    width=650,
    height=248,
    hide_index=True
)


col1, col2, col3 = st.columns(3)


with col1:

    metric_card(
        "🔢",
        "64 → 32",
        "LSTM Units"
    )


with col2:

    metric_card(
        "⚙️",
        "Adam",
        "Optimizer"
    )


with col3:

    metric_card(
        "📉",
        "MSE",
        "Loss Function"
    )


# ================================================================
# TRAINING CONFIGURATION
# ================================================================

section_header(
    "Model Training Configuration",
    "Configuration used during the LSTM training process.",
    "🏋️"
)


training_df = pd.DataFrame(
    {
        "Parameter": [
            "Epochs",
            "Batch size",
            "Steps per epoch",
            "Validation steps",
            "Optimizer",
            "Loss",
            "Metric",
            "Early stopping patience",
            "Learning-rate reduction patience"
        ],

        "Value": [
            "30",
            "128",
            "3,012",
            "753",
            "Adam",
            "MSE",
            "MAE",
            "5",
            "2"
        ]
    }
)


st.dataframe(
    training_df,
    width=550,
    height=352,
    #use_container_width=True,
    hide_index=True
)


# ================================================================
# TRAINING RESULTS
# ================================================================

section_header(
    "LSTM Training Performance",
    "Training and validation loss and MAE recorded during model training.",
    "📉"
)


col1, col2 = st.columns(2)


with col1:

    st.markdown(
        '<div class="chart-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        "### 📉 Training and Validation Loss"
    )

    show_chart(
        "lstm_training_validation_loss.png",
        "LSTM training and validation loss."
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        '<div class="chart-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        "### 📈 Training and Validation MAE"
    )

    show_chart(
        "lstm_training_validation_mae.png",
        "LSTM training and validation MAE."
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ================================================================
# TEST PERFORMANCE
# ================================================================

section_header(
    "LSTM Test Performance",
    "Multi-output regression performance of the trained model on the 2025 Colombo test dataset.",
    "🏆"
)


performance_df = pd.DataFrame(
    {
        "Weather Variable": [
            "Temperature",
            "Humidity",
            "Pressure",
            "Wind Speed",
            "Rainfall",
            "Wind Gust",
            "Cloud Cover",
            "Solar Radiation",
            "Dew Point"
        ],

        "MAE": [
            0.3367,
            1.9194,
            0.2604,
            1.6940,
            0.3198,
            2.7417,
            12.5586,
            30.7344,
            0.2781
        ],

        "RMSE": [
            0.4790,
            2.6345,
            0.3394,
            2.2942,
            0.8666,
            3.7010,
            19.0326,
            53.3159,
            0.3905
        ],

        "R²": [
            0.9503,
            0.9381,
            0.9624,
            0.8785,
            0.3243,
            0.9077,
            0.6395,
            0.9685,
            0.8906
        ]
    }
)


st.dataframe(
    performance_df.style.format(
        {
            "MAE": "{:.4f}",
            "RMSE": "{:.4f}",
            "R²": "{:.4f}"
        }
    ),
    width=750,
    height=352,
    #use_container_width=True,
    hide_index=True
)


# ================================================================
# METRIC CHARTS
# ================================================================

section_header(
    "Evaluation Metrics by Weather Variable",
    "Comparison of MAE, RMSE and R² across the nine prediction targets.",
    "📊"
)


col1, col2 = st.columns(2)


with col1:

    st.markdown(
        '<div class="chart-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        "### 📊 Mean Absolute Error"
    )

    show_chart(
        "lstm_mae_by_variable.png",
        "MAE for each predicted weather variable."
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        '<div class="chart-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        "### 📊 Root Mean Squared Error"
    )

    show_chart(
        "lstm_rmse_by_variable.png",
        "RMSE for each predicted weather variable."
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


st.markdown("<br>", unsafe_allow_html=True)


st.markdown(
    '<div class="chart-card">',
    unsafe_allow_html=True
)

st.markdown(
    "### 📊 R² Score by Weather Variable"
)

show_chart(
    "lstm_r2_by_variable.png",
    "R² score for each predicted weather variable."
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ================================================================
# PREDICTION RESULTS
# ================================================================

section_header(
    "Actual vs Predicted Results",
    "Comparison between observed and LSTM-predicted values for each weather variable.",
    "🔮"
)


prediction_charts = {

    "Temperature": "actual_predicted_temperature.png",

    "Humidity": "actual_predicted_humidity.png",

    "Pressure": "actual_predicted_pressure.png",

    "Wind Speed": "actual_predicted_windspeed.png",

    "Rainfall": "actual_predicted_rainfall.png",

    "Wind Gust": "actual_predicted_windgust.png",

    "Cloud Cover": "actual_predicted_cloudcover.png",

    "Solar Radiation": "actual_predicted_solarradiation.png",

    "Dew Point": "actual_predicted_dewpoint.png"

}


for i in range(
    0,
    len(prediction_charts),
    2
):

    items = list(
        prediction_charts.items()
    )[i:i + 2]

    col1, col2 = st.columns(2)

    for j, (
        variable,
        filename
    ) in enumerate(items):

        if j == 0:

            column = col1

        else:

            column = col2

        with column:

            st.markdown(
                '<div class="chart-card">',
                unsafe_allow_html=True
            )

            st.markdown(
                f"### 🌡️ {variable}"
            )

            show_chart(
                filename,
                f"Actual vs predicted {variable.lower()}."
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


# ================================================================
# ACTUAL VS PREDICTED SCATTER PLOTS
# ================================================================

section_header(
    "Actual vs Predicted Scatter Plots",
    "Scatter plots showing the relationship between actual and predicted values for each target variable.",
    "🎯"
)


scatter_charts = {

    "Temperature":
        "actual_vs_predicted_temperature.png",

    "Humidity":
        "actual_vs_predicted_humidity.png",

    "Pressure":
        "actual_vs_predicted_pressure.png",

    "Wind Speed":
        "actual_vs_predicted_windspeed.png",

    "Rainfall":
        "actual_vs_predicted_rainfall.png",

    "Wind Gust":
        "actual_vs_predicted_windgust.png",

    "Cloud Cover":
        "actual_vs_predicted_cloudcover.png",

    "Solar Radiation":
        "actual_vs_predicted_solarradiation.png",

    "Dew Point":
        "actual_vs_predicted_dewpoint.png"

}


for i in range(
    0,
    len(scatter_charts),
    2
):

    items = list(
        scatter_charts.items()
    )[i:i + 2]

    col1, col2 = st.columns(2)

    for j, (
        variable,
        filename
    ) in enumerate(items):

        column = (
            col1
            if j == 0
            else col2
        )

        with column:

            st.markdown(
                '<div class="chart-card">',
                unsafe_allow_html=True
            )

            st.markdown(
                f"### 🎯 {variable}"
            )

            show_chart(
                filename,
                f"Actual vs predicted scatter plot for {variable.lower()}."
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


# ================================================================
# RAIN / NO-RAIN PERFORMANCE
# ================================================================

section_header(
    "Rain / No-Rain Performance",
    "Classification performance obtained by converting rainfall predictions into rain/no-rain categories.",
    "🌧️"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    metric_card(
        "🎯",
        "72.51%",
        "Accuracy"
    )


with col2:

    metric_card(
        "🔵",
        "63.52%",
        "Precision"
    )


with col3:

    metric_card(
        "🟢",
        "86.15%",
        "Recall"
    )


with col4:

    metric_card(
        "⭐",
        "73.13%",
        "F1 Score"
    )


# ================================================================
# CONFUSION MATRIX
# ================================================================

# # ================================================================
# CONFUSION MATRIX
# ================================================================

section_header(
    "Rain / No-Rain Confusion Matrix",
    "Confusion matrix showing the LSTM model's performance "
    "in distinguishing between rainfall and non-rainfall conditions.",
    "🌧️"
)

# Center the confusion matrix and reduce its size
col1, col2, col3 = st.columns([1, 2, 1])

with col2:

    st.image(
        os.path.join(
            ASSETS_DIR,
            "rain_no_rain_confusion_matrix.png"
        ),
        width=430
    )

    st.caption(
        "Rain / No-Rain classification confusion matrix."
    )

# ================================================================
# FINAL SUMMARY
# ================================================================

section_header(
    "Model Summary",
    "Overall summary of the Colombo district next-hour forecasting experiment.",
    "📌"
)


st.markdown(
    """
    <div class="section-card">

    <h3>🤖 Colombo LSTM Forecasting System</h3>

    <p>
    The trained LSTM model uses the previous 24 hours of
    Colombo weather observations to predict nine weather
    variables for the following hour.
    </p>

    <p>
    The model was trained using observations from 2020–2023,
    validated using 2024 observations and evaluated using
    unseen 2025 observations.
    </p>

    <p>
    The evaluation demonstrates strong predictive performance
    for several variables, particularly solar radiation,
    pressure and temperature, while rainfall and cloud cover
    remain more challenging prediction targets.
    </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ================================================================
# FOOTER
# ================================================================

show_footer()