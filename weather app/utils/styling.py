import streamlit as st

def apply_dashboard_style():
    st.markdown(
        """
        <style>
        /* ========================================================
           GLOBAL DARK BACKGROUND & BASE TYPOGRAPHY
        ======================================================== */
        .stApp {
            background-color: #0A0F1D !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        }

        .main .block-container {
            max-width: 1280px !important;
            padding-top: 2rem !important;
            padding-bottom: 3rem !important;
        }

        /* Reset default Streamlit wrapper styles */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
        }

        /* High-contrast White/Light Headings & Paragraphs */
        .stApp h1, .stApp h2, .stApp h3, .stApp h4,
        div[data-testid="stMarkdownContainer"] h1,
        div[data-testid="stMarkdownContainer"] h2,
        div[data-testid="stMarkdownContainer"] h3,
        div[data-testid="stMarkdownContainer"] h4 {
            color: #F8FAFC !important;
            font-weight: 800 !important;
            letter-spacing: -0.02em !important;
        }

        .stApp p, .stApp span, .stApp label,
        div[data-testid="stMarkdownContainer"] p {
            color: #94A3B8 !important;
        }

        /* ========================================================
           SIDEBAR STYLING (DEEP OBSIDIAN & NAVY)
        ======================================================== */
        section[data-testid="stSidebar"] {
            background: #060A12 !important;
            border-right: 1px solid #1E293B !important;
        }

        section[data-testid="stSidebar"] * {
            color: #F8FAFC !important;
        }

        section[data-testid="stSidebar"] .stCaption {
            color: #38BDF8 !important;
        }

        section[data-testid="stSidebar"] hr {
            border: none !important;
            border-top: 1px solid #1E293B !important;
            margin: 1.2rem 0 !important;
        }

        /* Hide native Streamlit UI elements */
        #MainMenu, footer, header {
            visibility: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# ================================================================
# HERO SECTION
# ================================================================
def show_hero(title, subtitle, icon="⚡"):
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #111827 0%, #1E3A8A 100%);
            border: 1px solid #2563EB;
            border-radius: 16px;
            padding: 1.75rem 2rem;
            margin-bottom: 1.75rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
            position: relative;
            overflow: hidden;
        ">
            <div style="
                position: absolute;
                top: 0; left: 0; right: 0;
                height: 3px;
                background: linear-gradient(90deg, #38BDF8, #2563EB, #60A5FA);
            "></div>
            <h1 style="margin: 0 0 0.5rem 0; color: #FFFFFF !important; font-size: 1.85rem; font-weight: 800; letter-spacing: -0.02em;">
                <span style="margin-right: 0.5rem;">{icon}</span>{title}
            </h1>
            <p style="margin: 0; color: #93C5FD !important; font-size: 1.05rem; font-weight: 400;">
                <span style="color: #38BDF8 !important; margin-right: 0.35rem;">✦</span>{subtitle}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ================================================================
# METRIC CARD
# ================================================================
def metric_card(icon, value, label):
    st.markdown(
        f"""
        <div style="
            background: #111827;
            border: 1px solid #1F2937;
            border-radius: 14px;
            padding: 1.35rem 1rem;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
            position: relative;
            overflow: hidden;
            margin-bottom: 1rem;
        ">
            <div style="
                position: absolute;
                top: 0; left: 0; right: 0;
                height: 3px;
                background: linear-gradient(90deg, #2563EB, #38BDF8);
            "></div>
            <div style="font-size: 1.9rem; margin-bottom: 0.2rem;">{icon}</div>
            <div style="font-size: 1.7rem; font-weight: 800; color: #60A5FA !important; line-height: 1.2;">{value}</div>
            <div style="font-size: 0.78rem; font-weight: 700; color: #94A3B8 !important; text-transform: uppercase; letter-spacing: 0.06em; margin-top: 0.4rem;">
                <span style="color: #38BDF8 !important; margin-right: 0.2rem;">●</span>{label}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ================================================================
# FEATURE CARD
# ================================================================
def feature_card(title, description, icon="💎"):
    st.markdown(
        f"""
        <div style="
            background: #111827;
            border: 1px solid #1F2937;
            border-left: 4px solid #3B82F6;
            border-radius: 12px;
            padding: 1.35rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            margin-bottom: 1rem;
            height: 100%;
        ">
            <h3 style="margin: 0 0 0.5rem 0; font-size: 1.15rem; color: #F8FAFC !important; font-weight: 750;">
                <span style="margin-right: 0.4rem;">{icon}</span>{title}
            </h3>
            <p style="margin: 0; color: #94A3B8 !important; font-size: 0.92rem; line-height: 1.55;">{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ================================================================
# INFO CARD
# ================================================================
def info_card(title, content, icon="ℹ️"):
    st.markdown(
        f"""
        <div style="
            background: #111827;
            border: 1px solid #1F2937;
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        ">
            <h3 style="margin: 0 0 0.5rem 0; font-size: 1.1rem; color: #F8FAFC !important; font-weight: 700;">
                <span style="margin-right: 0.4rem;">{icon}</span>{title}
            </h3>
            <p style="margin: 0; color: #94A3B8 !important; font-size: 0.92rem; line-height: 1.5;">{content}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ================================================================
# SECTION HEADER
# ================================================================
def section_header(title, description=None, icon="💠"):
    desc_html = f"<p style='margin: 0.3rem 0 1.25rem 0; color: #94A3B8 !important; font-size: 0.95rem;'>{description}</p>" if description else ""
    st.markdown(
        f"""
        <div style="margin-top: 1.75rem; margin-bottom: 0.5rem;">
            <h2 style="margin: 0; font-size: 1.4rem; color: #F8FAFC !important; font-weight: 800; display: flex; align-items: center; gap: 0.4rem;">
                <span>{icon}</span>
                <span>{title}</span>
            </h2>
            {desc_html}
        </div>
        """,
        unsafe_allow_html=True
    )

# ================================================================
# FOOTER
# ================================================================
def show_footer():
    st.markdown(
        """
        <hr style="border: none; border-top: 1px solid #1E293B; margin: 2rem 0 1.5rem 0;" />
        <div style="
            background: #0B0F19;
            border: 1px solid #1E293B;
            border-radius: 12px;
            padding: 1.25rem;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        ">
            <p style="font-weight: 800; color: #F8FAFC !important; margin: 0 0 0.25rem 0; font-size: 1rem;">
                🌦️ Sri Lanka Weather Analysis & Forecasting System
            </p>
            <p style="color: #38BDF8 !important; font-size: 0.85rem; font-weight: 600; margin: 0 0 0.35rem 0;">
                🎓 BSc (Hons) Data Science Capstone Project
            </p>
            <p style="color: #64748B !important; font-size: 0.78rem; margin: 0;">
                📊 Historical Weather Analysis &nbsp;•&nbsp; 🧠 LSTM Next-Hour Forecasting
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )