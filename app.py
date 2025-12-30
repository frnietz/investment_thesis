import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(
    page_title="ThesisOS",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>

/* --- Global --- */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #0E1117;
    color: #E6E6E6;
}

/* Remove Streamlit junk */
#MainMenu, footer, header {
    visibility: hidden;
}

/* Headings */
h1, h2, h3 {
    font-weight: 600;
    letter-spacing: -0.02em;
}

/* --- Cards --- */
.card {
    background: #161B22;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 0 0 1px rgba(255,255,255,0.04);
}

/* --- Metric Cards --- */
.metric {
    background: #161B22;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
}

.metric-title {
    font-size: 13px;
    color: #8B949E;
}

.metric-value {
    font-size: 20px;
    font-weight: 600;
    margin-top: 4px;
}

/* --- Inputs --- */
input, textarea, select {
    background-color: #0E1117 !important;
    border-radius: 10px !important;
    border: 1px solid #30363D !important;
    color: #E6E6E6 !important;
}

/* --- Buttons --- */
.stButton>button {
    background: linear-gradient(135deg, #3B82F6, #2563EB);
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 18px;
    font-weight: 600;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #2563EB, #1D4ED8);
}

/* --- Tabs --- */
.stTabs [data-baseweb="tab"] {
    font-size: 14px;
    padding: 12px;
    color: #8B949E;
}

.stTabs [aria-selected="true"] {
    color: #E6E6E6;
    border-bottom: 2px solid #3B82F6;
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="card">
    <h2>📊 ThesisOS</h2>
    <p style="color:#8B949E;">Investment Thesis Builder</p>
</div>
""", unsafe_allow_html=True)


st.markdown("<div class='card'>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 1, 1])

ticker = col1.text_input("Ticker", placeholder="AAPL, MSFT, NVDA")
horizon = col2.selectbox("Time Horizon", ["Short", "Medium", "Long"])
generate = col3.button("Generate Thesis")

st.markdown("</div>", unsafe_allow_html=True)

if generate and ticker:
    col1, col2, col3, col4 = st.columns(4)

    col1.markdown("""
    <div class="metric">
        <div class="metric-title">Sector</div>
        <div class="metric-value">Technology</div>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown("""
    <div class="metric">
        <div class="metric-title">Macro Regime</div>
        <div class="metric-value">Late Cycle</div>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown("""
    <div class="metric">
        <div class="metric-title">Commodity Exposure</div>
        <div class="metric-value">Energy</div>
    </div>
    """, unsafe_allow_html=True)

    col4.markdown("""
    <div class="metric">
        <div class="metric-title">Supply Chain Stress</div>
        <div class="metric-value">Medium</div>
    </div>
    """, unsafe_allow_html=True)


    tabs = st.tabs([
        "🌍 Macro",
        "🛢️ Commodities",
        "🏭 Supply Chain",
        "📊 Financials",
        "⚠️ Risks",
        "✅ Decision"
    ])

    with tabs[0]:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.selectbox("Inflation Trend", ["Rising", "Falling", "Sticky"])
        st.selectbox("Rates Outlook", ["Tightening", "Neutral", "Easing"])
        st.text_area("Key Macro Insight", placeholder="What really matters here?")
        st.markdown("</div>", unsafe_allow_html=True)


    with tabs[1]:
        st.write("Commodity Exposure")
        st.multiselect("Key Inputs", ["Oil", "Gas", "Copper", "Agriculture"])

    with tabs[2]:
        st.slider("Supply Chain Pressure", 1, 5, 3)
        st.text_area("Key Bottlenecks")

    with tabs[3]:
        st.metric("Gross Margin", f"{info.get('grossMargins', 0)*100:.1f}%")
        st.metric("Debt / Equity", info.get("debtToEquity", "N/A"))

    with tabs[4]:
        st.text_area("Key Risks")

    with tabs[5]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    decision = st.selectbox("Final Decision", ["Accumulate", "Watch", "Avoid"])
    confidence = st.slider("Confidence Level", 1, 5, 3)
    thesis = st.text_area(
        "Final Thesis Summary",
        placeholder="Clear, structured, unemotional reasoning..."
    )

    st.button("Save Thesis")

    st.markdown("</div>", unsafe_allow_html=True)

