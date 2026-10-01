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
    page_title="Model Results",
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
        # 🤖 Models
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

        **🤖 Models**  
        LSTM, LightGBM, RF Classifier

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
    "Colombo Weather Forecasting Model",
    "Model architecture, training process, evaluation results and prediction performance",
    "🤖"
)


# ================================================================
# MODEL OVERVIEW
# ================================================================

section_header(
    "Model Overview",
    "Summary of the Colombo district LSTM forecasting experiment and rainfall forecasting experiment using a Random Forest Classifier and LightGBM Regressor.",
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
    "The LSTM and LightGBM models were trained using hourly observations from the Colombo district.",
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
        "96,060",
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
# RAIN / NO-RAIN CLASSIFICATION PERFORMANCE
# ================================================================

section_header(
    "Rain / No-Rain Classification Performance",
    "Comparison of classification performance for rainfall occurrence prediction using Random Forest, XGBoost and LightGBM.",
    "🌧️"
)

classification_df = pd.DataFrame(
    {
        "Model": [
            "Random Forest",
            "XGBoost",
            "LightGBM"
        ],
        "Precision": [
            0.7885,
            0.6723,
            0.7636
        ],
        "Recall": [
            0.8231,
            0.9086,
            0.7897
        ],
        "F1-Score": [
            0.8054,
            0.7728,
            0.7764
        ],
        "ROC-AUC": [
            0.9007,
            0.8897,
            0.8823
        ]
    }
)

st.dataframe(
    classification_df.style.format(
        {
            "Precision": "{:.4f}",
            "Recall": "{:.4f}",
            "F1-Score": "{:.4f}",
            "ROC-AUC": "{:.4f}"
        }
    ),
    use_container_width=True,
    hide_index=True
)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card(
        "🎯",
        "90.07%",
        "RF ROC-AUC"
    )

with col2:
    metric_card(
        "🔵",
        "78.85%",
        "RF Precision"
    )

with col3:
    metric_card(
        "🟢",
        "82.31%",
        "RF Recall"
    )

with col4:
    metric_card(
        "⭐",
        "80.54%",
        "RF F1-Score"
    )


# ================================================================
# RAINFALL MODEL COMBINATION PERFORMANCE
# ================================================================

section_header(
    "Rainfall Model Combination Performance",
    "Performance of the two-stage rainfall prediction system using different classifier and regression model combinations.",
    "🔄"
)

combination_df = pd.DataFrame(
    {
        "Combination": [
            "RF + RF",
            "RF + XGB",
            "RF + LGBM",
            "XGB + RF",
            "XGB + XGB",
            "XGB + LGBM",
            "LGBM + RF",
            "LGBM + XGB",
            "LGBM + LGBM"
        ],
        "F1": [
            0.8054,
            0.8054,
            0.8054,
            0.7728,
            0.7728,
            0.7728,
            0.7764,
            0.7764,
            0.7764
        ],
        "ROC-AUC": [
            0.9007,
            0.9007,
            0.9007,
            0.8897,
            0.8897,
            0.8897,
            0.8823,
            0.8823,
            0.8823
        ],
        "MAE (mm)": [
            0.2925,
            0.2710,
            0.2676,
            0.3228,
            0.2929,
            0.2892,
            0.2945,
            0.2733,
            0.2699
        ],
        "RMSE (mm)": [
            0.7636,
            0.7140,
            0.7024,
            0.7688,
            0.7142,
            0.7017,
            0.7645,
            0.7179,
            0.7065
        ],
        "R²": [
            0.4754,
            0.5413,
            0.5561,
            0.4683,
            0.5412,
            0.5570,
            0.4742,
            0.5363,
            0.5510
        ],
        "Heavy Rain F1": [
            0.3434,
            0.4300,
            0.3906,
            0.3434,
            0.4300,
            0.3906,
            0.3469,
            0.4300,
            0.3906
        ]
    }
)

st.dataframe(
    combination_df.style.format(
        {
            "F1": "{:.4f}",
            "ROC-AUC": "{:.4f}",
            "MAE (mm)": "{:.4f}",
            "RMSE (mm)": "{:.4f}",
            "R²": "{:.4f}",
            "Heavy Rain F1": "{:.4f}"
        }
    ),
    use_container_width=True,
    hide_index=True
)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    metric_card(
        "📉",
        "0.2676 mm",
        "Lowest MAE - RF + LGBM"
    )

with col2:
    metric_card(
        "📊",
        "0.5570",
        "Highest R² - XGB + LGBM"
    )

with col3:
    metric_card(
        "🌧️",
        "0.4300",
        "Highest Heavy Rain F1"
    )


# ================================================================
# RAIN / NO-RAIN CONFUSION MATRIX
# ================================================================

section_header(
    "Rain / No-Rain Confusion Matrix",
    "Confusion matrix showing the Random Forest Classifier's performance in distinguishing between rainfall and non-rainfall conditions.",
    "🌧️"
)

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
# GEOGRAPHICAL POINT-WISE EVALUATION
# ================================================================

section_header(
    "Geographical Point-wise Evaluation",
    "LSTM prediction performance across the 11 geographical points within the Colombo District.",
    "📍"
)

geo_df = pd.DataFrame(
    {
        "Point": [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
        ],
        "Latitude": [
            6.85991, 6.85991, 6.85991,
            6.92710, 6.92710, 6.92710,
            6.92710, 6.92710,
            6.99429, 6.99429, 6.99429
        ],
        "Longitude": [
            79.79351, 79.86120, 79.92889,
            79.72583, 79.79351, 79.86120,
            79.92889, 79.99657,
            79.79351, 79.86120, 79.92889
        ],
        "Overall Mean R²": [
            0.8525,
            0.8518,
            0.8515,
            0.7976,
            0.8525,
            0.8524,
            0.8525,
            0.8338,
            0.8566,
            0.8566,
            0.8566
        ],
        "Overall NRMSE": [
            0.0552,
            0.0544,
            0.0545,
            0.0601,
            0.0552,
            0.0552,
            0.0552,
            0.0564,
            0.0546,
            0.0546,
            0.0546
        ],
        "Overall Accuracy (%)": [
            94.48,
            94.56,
            94.55,
            93.99,
            94.48,
            94.49,
            94.48,
            94.36,
            94.54,
            94.54,
            94.54
        ]
    }
)

st.dataframe(
    geo_df.style.format(
        {
            "Latitude": "{:.5f}",
            "Longitude": "{:.5f}",
            "Overall Mean R²": "{:.4f}",
            "Overall NRMSE": "{:.4f}",
            "Overall Accuracy (%)": "{:.2f}"
        }
    ),
    use_container_width=True,
    hide_index=True
)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    metric_card(
        "📍",
        "11",
        "Geographical Points"
    )

with col2:
    metric_card(
        "📈",
        "94.56%",
        "Highest Accuracy"
    )

with col3:
    metric_card(
        "📊",
        "93.99%",
        "Lowest Accuracy"
    )
# ================================================================
# POINT-WISE OVERALL ACCURACY INDEX CHART
# ================================================================

st.markdown(
    """
    <div class="section-card">
    <h3>📊 Point-wise Overall Accuracy Index</h3>
    </div>
    """,
    unsafe_allow_html=True
)
st.image(
        os.path.join(
            ASSETS_DIR,
            "pointwise_overall_accuracy.png"
        ),
        use_container_width=True
    )

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="section-card">

    <h3>📌 Geographical Evaluation Summary</h3>

    <p>
    The LSTM RF+LGBM models was evaluated across 11 geographical points
    within the Colombo District using unseen 2025 test observations.
    The overall accuracy index ranged from <b>93.99%</b> to
    <b>94.56%</b>, indicating relatively consistent prediction
    performance across the evaluated locations.
    </p>

    </div>
    """,
    unsafe_allow_html=True
)

# ================================================================
# FINAL SUMMARY
# ================================================================

section_header(
    "<h3>📌Model Summary</h3>",
    "Overall summary of the Colombo district next-hour forecasting experiment.",
    
)


st.markdown(
    """
    <div class="section-card">

    <h3>🤖 Colombo Weather Forecasting System</h3>

    <p>
    The trained LSTM and LightGBM models use the previous 24 hours of
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