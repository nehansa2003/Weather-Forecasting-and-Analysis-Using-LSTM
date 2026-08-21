# 🌦️ Sri Lanka Weather Prediction & Analysis

This repository contains my **BSc (Hons) Data Science Capstone Project** for weather analysis and next-hour weather forecasting in Sri Lanka.

## 📌 Project Overview

The project analyzes hourly weather data from **2020–2025** for five Sri Lankan districts:

- Colombo
- Gampaha
- Galle
- Kandy
- Jaffna

The project includes historical weather analysis and an **LSTM-based multi-output model** for predicting the next hour's weather in Colombo.

## 🤖 Forecasting Model

The LSTM model uses the previous **24 hours** of weather observations to predict the next hour:

- Temperature
- Humidity
- Pressure
- Wind Speed
- Rainfall
- Wind Gust
- Cloud Cover
- Solar Radiation
- Dew Point

The model was trained using:
- **2020–2023:** Training
- **2024:** Validation
- **2025:** Testing

## 🌐 Weather Dashboard

A Streamlit web application is included in the `weather_app` folder.

The dashboard provides:

- 📊 Historical weather analysis
- 📍 Geographical point selection
- 🌦️ Current weather information
- 🤖 Colombo next-hour weather forecasting
- 📈 Model training and evaluation results
- 🌧️ Rain/no-rain performance analysis

The forecasting system identifies the nearest predefined Colombo geographical point and uses the previous 24 hours of weather data for prediction.

🛠️ Technologies

Python • Pandas • NumPy • Scikit-learn • TensorFlow/Keras • Streamlit • Matplotlib • Seaborn • Open-Meteo API

## 📁 Repository Structure

```text
weather_project/
│
├── notebooks/
│   └── Weather Analysis & Model Training
│
├── weather_app/
│   ├── pages/
│   ├── services/
│   ├── utils/
│   ├── models/
│   ├── assets/
│   └── app.py
│
└── README.md

