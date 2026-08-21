import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# Set Seaborn visual style
sns.set_theme(style="whitegrid")

# ================================================================
# IMPORT PROJECT MODULES
# ================================================================

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from utils.constants import (
    DATA_PATH,
    WEATHER_VARIABLES,
    DISTRICT_AVERAGE_VARIABLES,
    HOURLY_VARIABLES,
    YEARLY_VARIABLES,
    SEASONAL_VARIABLES,
    MONTHLY_VARIABLES,
    CORRELATION_VARIABLES,
    RELATIONSHIP_PAIRS,
    VARIABLE_LABELS,
    RAIN_THRESHOLD
)

from utils.styling import (
    apply_dashboard_style,
    show_hero,
    metric_card,
    info_card,
    show_footer
)

# ================================================================
# PAGE CONFIGURATION
# ================================================================

st.set_page_config(
    page_title="Weather Analysis",
    page_icon="📈",
    layout="wide"
)
apply_dashboard_style()

# ================================================================
# LOAD DATA
# ================================================================

@st.cache_data
def load_data():
    df = pd.read_parquet(DATA_PATH, engine="pyarrow")
    
    df["datetime"] = pd.to_datetime(df["datetime"])
    
    if "hour" not in df.columns:
        df["hour"] = df["datetime"].dt.hour
    if "year" not in df.columns:
        df["year"] = df["datetime"].dt.year
    if "month" not in df.columns:
        df["month"] = df["datetime"].dt.month
        
    return df

weather_df = load_data()

# ================================================================
# TITLE
# ================================================================

show_hero(
    "Interactive Weather Analysis",
    "Interactive analysis of hourly weather observations (2020–2025).",
    "📈"
)
# st.title("📈 Interactive Weather Analysis")
# st.markdown("Interactive analysis of hourly weather observations (2020–2025).")

# ================================================================
# SIDEBAR FILTER
# ================================================================

st.sidebar.header("Analysis Filters")

# District Filter
if "district" in weather_df.columns:
    district_options = ["All Districts"] + sorted(weather_df["district"].dropna().unique().tolist())
    selected_district = st.sidebar.selectbox("Select District", district_options)
else:
    selected_district = "All Districts"

# Year Filter
if "year" in weather_df.columns:
    available_years = sorted(weather_df["year"].dropna().unique().tolist())
    selected_years = st.sidebar.slider(
        "Select Year Range",
        min_value=int(min(available_years)),
        max_value=int(max(available_years)),
        value=(int(min(available_years)), int(max(available_years)))
    )
else:
    selected_years = None

# Filter logic
analysis_df = weather_df.copy()

if selected_district != "All Districts":
    analysis_df = analysis_df[analysis_df["district"] == selected_district]

if selected_years:
    analysis_df = analysis_df[
        (analysis_df["year"] >= selected_years[0]) & 
        (analysis_df["year"] <= selected_years[1])
    ]

st.sidebar.metric("Filtered Records", f"{len(analysis_df):,}")

# ================================================================
# TABS
# ================================================================

tabs = st.tabs([
    "📊 District Average",
    "🕐 Hourly",
    "📅 Yearly",
    "🌧️ Seasonal",
    "📆 Monthly",
    "📈 Time Series",
    "🔥 Heatmaps",
    "🔗 Correlation",
    "🗺️ Spatial",
    "📉 Relationships",
    "🌧️ Rain Probability",
    "📊 Distributions"
])


# ================================================================
# PAGE FOOTER
# ================================================================
show_footer()

# ################################################################
# 1. DISTRICT-WISE AVERAGE
# ################################################################
with tabs[0]:
    st.header("District-Wise Average Analysis")
    
    if "district" in weather_df.columns:
        available_variables = [col for col in DISTRICT_AVERAGE_VARIABLES if col in weather_df.columns]
        
        district_average = (
            analysis_df.groupby("district")[available_variables]
            .mean()
            .reset_index()
        )
        
        st.dataframe(district_average.round(3), use_container_width=True, hide_index=True)
        
        st.subheader("Visualization")
        variable = st.selectbox(
            "Select Weather Variable to Plot",
            available_variables,
            format_func=lambda x: VARIABLE_LABELS.get(x, (x, x))[0],
            key="dist_avg_var"
        )
        
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=district_average, x="district", y=variable, ax=ax, palette="viridis")
        
        var_name, var_unit = VARIABLE_LABELS.get(variable, (variable, variable))
        ax.set_title(f"Average {var_name} by District")
        ax.set_xlabel("District")
        ax.set_ylabel(var_unit)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("District metadata not available in dataset.")

# ################################################################
# 2. HOURLY ANALYSIS
# ################################################################
with tabs[1]:
    st.header("Average Hourly Weather Dynamics")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        var_primary = st.selectbox(
            "Primary Variable (Left Y-Axis)", 
            HOURLY_VARIABLES, 
            index=0,
            format_func=lambda x: VARIABLE_LABELS.get(x, (x, x))[0],
            key="hourly_v1"
        )
    with col2:
        secondary_options = ["None"] + HOURLY_VARIABLES
        var_secondary = st.selectbox(
            "Secondary Variable (Right Y-Axis - Optional)", 
            secondary_options, 
            index=0,
            format_func=lambda x: "None (Single Variable View)" if x == "None" else VARIABLE_LABELS.get(x, (x, x))[0],
            key="hourly_v2"
        )

    # 1. SINGLE VARIABLE VIEW
    if var_secondary == "None" or var_primary == var_secondary:
        fig, ax = plt.subplots(figsize=(12, 5))
        
        if selected_district == "All Districts" and "district" in analysis_df.columns:
            hourly_df = analysis_df.groupby(["hour", "district"])[var_primary].mean().reset_index()
            sns.lineplot(
                data=hourly_df,
                x="hour",
                y=var_primary,
                hue="district",
                marker="o",
                ax=ax
            )
            ax.set_title(f"24-Hour Diurnal Cycle by District: {VARIABLE_LABELS[var_primary][0]}")
        else:
            hourly_df = analysis_df.groupby("hour")[var_primary].mean().reset_index()
            ax.plot(
                hourly_df["hour"], 
                hourly_df[var_primary], 
                color="tab:red", 
                marker="o", 
                linewidth=2,
                label=VARIABLE_LABELS[var_primary][0]
            )
            ax.set_title(f"24-Hour Diurnal Cycle: {VARIABLE_LABELS[var_primary][0]}")

        ax.set_xlabel("Hour of Day (0 - 23)")
        ax.set_ylabel(VARIABLE_LABELS[var_primary][1])
        ax.set_xticks(range(0, 24))
        ax.grid(True, linestyle="--", alpha=0.6)
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # 2. DUAL VARIABLE VIEW
    else:
        hourly_df = analysis_df.groupby("hour")[[var_primary, var_secondary]].mean().reset_index()
        fig, ax1 = plt.subplots(figsize=(12, 5))
        
        ax1.plot(hourly_df["hour"], hourly_df[var_primary], color="tab:red", marker="o", linewidth=2)
        ax1.set_xlabel("Hour of Day (0 - 23)")
        ax1.set_ylabel(VARIABLE_LABELS[var_primary][1], color="tab:red")
        ax1.set_xticks(range(0, 24))
        ax1.tick_params(axis="y", labelcolor="tab:red")
        
        ax2 = ax1.twinx()
        ax2.plot(hourly_df["hour"], hourly_df[var_secondary], color="tab:blue", marker="s", linewidth=2, linestyle="--")
        ax2.set_ylabel(VARIABLE_LABELS[var_secondary][1], color="tab:blue")
        ax2.tick_params(axis="y", labelcolor="tab:blue")
        ax2.grid(False)
        
        plt.title(f"Diurnal Comparison: {VARIABLE_LABELS[var_primary][0]} vs {VARIABLE_LABELS[var_secondary][0]}")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

# ################################################################
# 3. YEARLY ANALYSIS
# ################################################################
with tabs[2]:
    st.header("Year-Wise Weather Trends")
    
    yearly_variable = st.selectbox(
        "Select Weather Variable",
        [v for v in YEARLY_VARIABLES if v in analysis_df.columns],
        format_func=lambda x: VARIABLE_LABELS.get(x, (x, x))[0],
        key="yearly_var"
    )
    
    if "district" in analysis_df.columns:
        yearly_data = analysis_df.groupby(["district", "year"])[yearly_variable].mean().reset_index()
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=yearly_data, x="year", y=yearly_variable, hue="district", marker="o", ax=ax)
    else:
        yearly_data = analysis_df.groupby("year")[yearly_variable].mean().reset_index()
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=yearly_data, x="year", y=yearly_variable, marker="o", ax=ax)
        
    ax.set_title(f"Yearly Average: {VARIABLE_LABELS[yearly_variable][0]}")
    ax.set_ylabel(VARIABLE_LABELS[yearly_variable][1])
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# ################################################################
# 4. SEASONAL ANALYSIS
# ################################################################
with tabs[3]:
    st.header("Seasonal Weather Analysis")
    
    if "season" in analysis_df.columns:
        seasonal_variable = st.selectbox(
            "Select Variable",
            [v for v in SEASONAL_VARIABLES if v in analysis_df.columns],
            format_func=lambda x: VARIABLE_LABELS.get(x, (x, x))[0],
            key="seasonal_var"
        )
        
        fig, ax = plt.subplots(figsize=(10, 5))
        if "district" in analysis_df.columns and selected_district == "All Districts":
            sns.barplot(data=analysis_df, x="season", y=seasonal_variable, hue="district", errorbar=None, ax=ax)
        else:
            sns.barplot(data=analysis_df, x="season", y=seasonal_variable, errorbar=None, ax=ax)
            
        ax.set_title(f"Seasonal Comparison: {VARIABLE_LABELS[seasonal_variable][0]}")
        ax.set_ylabel(VARIABLE_LABELS[seasonal_variable][1])
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Season column is not present in the current dataset.")

# ################################################################
# 5. MONTHLY ANALYSIS
# ################################################################
with tabs[4]:
    st.header("Monthly Weather Profiles")
    
    monthly_var = st.selectbox(
        "Select Weather Variable",
        [v for v in MONTHLY_VARIABLES if v in analysis_df.columns],
        format_func=lambda x: VARIABLE_LABELS.get(x, (x, x))[0],
        key="monthly_profile_var"
    )
    
    fig, ax = plt.subplots(figsize=(10, 5))
    if "district" in analysis_df.columns and selected_district == "All Districts":
        sns.lineplot(data=analysis_df, x="month", y=monthly_var, hue="district", errorbar=None, marker="o", ax=ax)
    else:
        sns.lineplot(data=analysis_df, x="month", y=monthly_var, errorbar=None, marker="o", ax=ax)
        
    ax.set_xticks(range(1, 13))
    ax.set_title(f"Average Monthly Profile: {VARIABLE_LABELS[monthly_var][0]}")
    ax.set_ylabel(VARIABLE_LABELS[monthly_var][1])
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# ################################################################
# 6. MONTHLY TIME SERIES
# ################################################################
with tabs[5]:
    st.header("Long-Term Monthly Time Series")
    
    ts_variable = st.selectbox(
        "Select Weather Variable",
        [v for v in MONTHLY_VARIABLES if v in analysis_df.columns],
        format_func=lambda x: VARIABLE_LABELS.get(x, (x, x))[0]
    )
    
    if selected_district == "All Districts" and "district" in analysis_df.columns:
        monthly_trends = (
            analysis_df.groupby(["year", "month", "district"])[ts_variable]
            .mean()
            .reset_index()
        )
        monthly_trends["year_month"] = pd.to_datetime(
            monthly_trends["year"].astype(str) + "-" + monthly_trends["month"].astype(str) + "-01"
        )
        
        fig, ax = plt.subplots(figsize=(12, 5))
        sns.lineplot(data=monthly_trends, x="year_month", y=ts_variable, hue="district", marker="o", ax=ax)
        
    else:
        monthly_trends = (
            analysis_df.groupby(["year", "month"])[ts_variable]
            .mean()
            .reset_index()
        )
        monthly_trends["year_month"] = pd.to_datetime(
            monthly_trends["year"].astype(str) + "-" + monthly_trends["month"].astype(str) + "-01"
        )
        
        fig, ax = plt.subplots(figsize=(12, 5))
        sns.lineplot(data=monthly_trends, x="year_month", y=ts_variable, color="tab:blue", marker="o", ax=ax)

    ax.set_title(f"Long-Term Monthly Trends: {VARIABLE_LABELS[ts_variable][0]}")
    ax.set_xlabel("Date")
    ax.set_ylabel(VARIABLE_LABELS[ts_variable][1])
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# ################################################################
# 7. HEATMAPS
# ################################################################
with tabs[6]:
    st.header("Multi-Dimensional Aggregations & Heatmaps")
    
    target_var = st.selectbox(
        "Select Target Variable for Heatmap",
        [v for v in WEATHER_VARIABLES if v in analysis_df.columns],
        format_func=lambda x: VARIABLE_LABELS.get(x, (x, x))[0]
    )
    
    group_y = st.selectbox("Group By (Y-Axis)", ["district", "season"] if "season" in analysis_df.columns else ["district"])
    group_x = st.selectbox("Group By (X-Axis)", ["year", "month", "hour"])
    
    if group_y in analysis_df.columns and group_x in analysis_df.columns:
        heatmap_data = (
            analysis_df.groupby([group_y, group_x])[target_var]
            .mean()
            .unstack()
        )
        
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        ax.set_title(f"Average {VARIABLE_LABELS[target_var][0]} ({group_y.title()} vs {group_x.title()})")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

# ################################################################
# 8. CORRELATION
# ################################################################
with tabs[7]:
    st.header("Pearson Correlation Matrix")
    
    available_vars = [var for var in CORRELATION_VARIABLES if var in analysis_df.columns]
    
    if available_vars:
        corr_matrix = analysis_df[available_vars].corr(method="pearson")
        
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, linewidths=0.5, ax=ax)
        ax.set_title("Pearson Correlation Matrix", fontsize=14)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

# ################################################################
# 9. SPATIAL ANALYSIS
# ################################################################
with tabs[8]:
    st.header("Geographical Points Distribution")
    
    spatial_cols = ["latitude", "longitude"]
    if all(col in analysis_df.columns for col in spatial_cols) and "district" in analysis_df.columns:
        
        # Subsample if dataset is too large to maintain fast rendering performance
        sample_size = min(10000, len(analysis_df))
        plot_df = analysis_df.sample(n=sample_size, random_state=42) if len(analysis_df) > 10000 else analysis_df

        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot every individual coordinate point colored by district
        sns.scatterplot(
            data=plot_df,
            x="longitude",
            y="latitude",
            hue="district",
            alpha=0.6,
            s=30,
            ax=ax
        )
        
        # Calculate centroids purely for placing clear text labels per district
        district_centers = (
            analysis_df.groupby("district")[spatial_cols]
            .mean()
            .reset_index()
        )
        
        for _, row in district_centers.iterrows():
            ax.annotate(
                row["district"], 
                (row["longitude"], row["latitude"]),
                textcoords="offset points", 
                xytext=(0, 5), 
                ha='center',
                fontsize=10,
                weight='bold',
                bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.7, ec="none")
            )
            
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_title("Geographical Point Distribution Across Districts")
        
        # Move legend outside to prevent cluttering the map area
        ax.legend(title="District", bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Geographical coordinates (latitude, longitude) and district column are required for spatial mapping.")


# ################################################################
# 10. RELATIONSHIPS
# ################################################################
with tabs[9]:
    st.header("Pairwise Relationship Dynamics & LOWESS Trend Lines")
    
    pair_labels = [f"{VARIABLE_LABELS[x][0]} vs {VARIABLE_LABELS[y][0]}" for x, y in RELATIONSHIP_PAIRS]
    selected_pair_idx = st.selectbox("Select Relationship Pair", range(len(RELATIONSHIP_PAIRS)), format_func=lambda i: pair_labels[i])
    
    x_col, y_col = RELATIONSHIP_PAIRS[selected_pair_idx]
    
    sample_size = st.slider("Sample Size for Scatter Plot", min_value=1000, max_value=min(20000, len(analysis_df)), value=5000, step=1000)
    sample_df = analysis_df.sample(n=min(sample_size, len(analysis_df)), random_state=42)
    
    fig, ax = plt.subplots(figsize=(9, 5))
    
    sns.regplot(
        data=sample_df, x=x_col, y=y_col, ax=ax,
        scatter_kws={"alpha": 0.2, "s": 12},
        line_kws={"color": "red", "linewidth": 2, "label": "Linear Fit"}
    )
    
    sns.regplot(
        data=sample_df, x=x_col, y=y_col, ax=ax, scatter=False, lowess=True,
        line_kws={"color": "blue", "linewidth": 2, "linestyle": "--", "label": "LOWESS Fit"}
    )
    
    ax.set_title(f"Dynamics: {VARIABLE_LABELS[x_col][0]} vs {VARIABLE_LABELS[y_col][0]}")
    ax.set_xlabel(VARIABLE_LABELS[x_col][1])
    ax.set_ylabel(VARIABLE_LABELS[y_col][1])
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# ################################################################
# 11. RAINFALL PROBABILITY
# ################################################################
with tabs[10]:
    st.header("Rainfall Probability Analysis")
    
    threshold = st.number_input("Rainfall Threshold (mm)", min_value=0.0, value=RAIN_THRESHOLD, step=0.1)
    group_dimension = st.radio("Group Probability By", ["hour", "month", "district"], horizontal=True)
    
    if "rainfall_mm" in analysis_df.columns and group_dimension in analysis_df.columns:
        
        fig, ax = plt.subplots(figsize=(10, 5))
        
        if selected_district == "All Districts" and group_dimension != "district" and "district" in analysis_df.columns:
            prob_df = (
                analysis_df.assign(rain_occurs=(analysis_df["rainfall_mm"] >= threshold))
                .groupby([group_dimension, "district"])["rain_occurs"]
                .mean()
                .mul(100)
                .reset_index(name="probability_pct")
            )
            sns.lineplot(data=prob_df, x=group_dimension, y="probability_pct", hue="district", marker="o", ax=ax)
        else:
            prob_df = (
                analysis_df.assign(rain_occurs=(analysis_df["rainfall_mm"] >= threshold))
                .groupby(group_dimension)["rain_occurs"]
                .mean()
                .mul(100)
                .reset_index(name="probability_pct")
            )
            if group_dimension == "district":
                sns.barplot(data=prob_df, x=group_dimension, y="probability_pct", ax=ax)
            else:
                sns.lineplot(data=prob_df, x=group_dimension, y="probability_pct", marker="o", ax=ax)
            
        ax.set_title(f"Rainfall Probability (>= {threshold}mm) by {group_dimension.title()}")
        ax.set_ylabel("Probability (%)")
        ax.set_ylim(0, 100)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

# ################################################################
# 12. DISTRIBUTIONS
# ################################################################
with tabs[11]:
    st.header("Variable Distributions")
    
    dist_var = st.selectbox(
        "Select Variable",
        [v for v in WEATHER_VARIABLES if v in analysis_df.columns],
        format_func=lambda x: VARIABLE_LABELS.get(x, (x, x))[0],
        key="dist_var_select"
    )
    
    bins = st.slider("Number of Bins", min_value=10, max_value=100, value=50)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(analysis_df[dist_var].dropna(), bins=bins, kde=True, ax=ax)
    
    ax.set_title(f"Distribution of {VARIABLE_LABELS[dist_var][0]}")
    ax.set_xlabel(VARIABLE_LABELS[dist_var][1])
    ax.set_ylabel("Count")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)



# ================================================================
# PAGE FOOTER
# ================================================================
#show_footer()