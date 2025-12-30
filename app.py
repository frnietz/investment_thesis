import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import datetime

# --- CONFIGURATION ---
st.set_page_config(
    page_title="MarketMap Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CONSTANTS & STATIC DATA ---
# Fetching "Sector" and "Market Cap" via yfinance for 50+ stocks is too slow for a web app.
# We hardcode the structural data (Sector, Weight) and fetch only Price Change live.
# Weights are approximate relative Market Caps.

STOCKS_DB = {
    "TR": [
        {"ticker": "THYAO.IS", "name": "Turk Hava Yollari", "sector": "Industrials", "mcap_weight": 350},
        {"ticker": "KCHOL.IS", "name": "Koc Holding", "sector": "Industrials", "mcap_weight": 320},
        {"ticker": "GARAN.IS", "name": "Garanti BBVA", "sector": "Financials", "mcap_weight": 310},
        {"ticker": "AKBNK.IS", "name": "Akbank", "sector": "Financials", "mcap_weight": 280},
        {"ticker": "ISCTR.IS", "name": "Is Bankasi", "sector": "Financials", "mcap_weight": 260},
        {"ticker": "TUPRS.IS", "name": "Tupras", "sector": "Energy", "mcap_weight": 250},
        {"ticker": "ASELS.IS", "name": "Aselsan", "sector": "Technology", "mcap_weight": 200},
        {"ticker": "BIMAS.IS", "name": "BIM Magazalar", "sector": "Consumer Defensive", "mcap_weight": 190},
        {"ticker": "SISE.IS", "name": "Sisecam", "sector": "Basic Materials", "mcap_weight": 160},
        {"ticker": "SAHOL.IS", "name": "Sabanci Holding", "sector": "Financials", "mcap_weight": 150},
        {"ticker": "EREGL.IS", "name": "Eregli Demir Celik", "sector": "Basic Materials", "mcap_weight": 145},
        {"ticker": "YKBNK.IS", "name": "Yapi Kredi", "sector": "Financials", "mcap_weight": 140},
        {"ticker": "FROTO.IS", "name": "Ford Otosan", "sector": "Consumer Cyclical", "mcap_weight": 130},
        {"ticker": "TCELL.IS", "name": "Turkcell", "sector": "Communication", "mcap_weight": 120},
        {"ticker": "ENKAI.IS", "name": "Enka Insaat", "sector": "Industrials", "mcap_weight": 110},
        {"ticker": "PETKM.IS", "name": "Petkim", "sector": "Basic Materials", "mcap_weight": 80},
        {"ticker": "TOASO.IS", "name": "Tofas", "sector": "Consumer Cyclical", "mcap_weight": 75},
        {"ticker": "ARCLK.IS", "name": "Arcelik", "sector": "Consumer Cyclical", "mcap_weight": 70},
        {"ticker": "MGROS.IS", "name": "Migros", "sector": "Consumer Defensive", "mcap_weight": 65},
        {"ticker": "PGSUS.IS", "name": "Pegasus", "sector": "Industrials", "mcap_weight": 60},
        {"ticker": "AEFES.IS", "name": "Anadolu Efes", "sector": "Consumer Defensive", "mcap_weight": 55},
        {"ticker": "TTKOM.IS", "name": "Turk Telekom", "sector": "Communication", "mcap_weight": 50},
        {"ticker": "ODAS.IS", "name": "Odas", "sector": "Utilities", "mcap_weight": 40},
        {"ticker": "SASA.IS", "name": "Sasa Polyester", "sector": "Basic Materials", "mcap_weight": 150},
        {"ticker": "HEKTS.IS", "name": "Hektas", "sector": "Basic Materials", "mcap_weight": 45},
    ],
    "UK": [
        {"ticker": "AZN.L", "name": "AstraZeneca", "sector": "Healthcare", "mcap_weight": 1800},
        {"ticker": "SHEL.L", "name": "Shell", "sector": "Energy", "mcap_weight": 1700},
        {"ticker": "HSBA.L", "name": "HSBC", "sector": "Financials", "mcap_weight": 1300},
        {"ticker": "ULVR.L", "name": "Unilever", "sector": "Consumer Defensive", "mcap_weight": 1000},
        {"ticker": "BP.L", "name": "BP", "sector": "Energy", "mcap_weight": 900},
        {"ticker": "RIO.L", "name": "Rio Tinto", "sector": "Basic Materials", "mcap_weight": 850},
        {"ticker": "GSK.L", "name": "GSK", "sector": "Healthcare", "mcap_weight": 700},
        {"ticker": "DGE.L", "name": "Diageo", "sector": "Consumer Defensive", "mcap_weight": 650},
        {"ticker": "REL.L", "name": "RELX", "sector": "Industrials", "mcap_weight": 600},
        {"ticker": "GLEN.L", "name": "Glencore", "sector": "Basic Materials", "mcap_weight": 580},
        {"ticker": "BATS.L", "name": "British Am. Tobacco", "sector": "Consumer Defensive", "mcap_weight": 550},
        {"ticker": "LSEG.L", "name": "LSE Group", "sector": "Financials", "mcap_weight": 500},
        {"ticker": "BARC.L", "name": "Barclays", "sector": "Financials", "mcap_weight": 350},
        {"ticker": "NG.L", "name": "National Grid", "sector": "Utilities", "mcap_weight": 400},
        {"ticker": "LLOY.L", "name": "Lloyds Banking", "sector": "Financials", "mcap_weight": 320},
        {"ticker": "VOD.L", "name": "Vodafone", "sector": "Communication", "mcap_weight": 250},
        {"ticker": "RR.L", "name": "Rolls-Royce", "sector": "Industrials", "mcap_weight": 280},
        {"ticker": "TSCO.L", "name": "Tesco", "sector": "Consumer Defensive", "mcap_weight": 220},
        {"ticker": "PRU.L", "name": "Prudential", "sector": "Financials", "mcap_weight": 200},
        {"ticker": "AAL.L", "name": "Anglo American", "sector": "Basic Materials", "mcap_weight": 350},
    ]
}

# Map UI period selection to yfinance period strings
PERIOD_MAP = {
    "1 Day": "2d", # Fetch 2 days to calculate 1 day change safely
    "5 Days": "5d",
    "1 Month": "1mo",
    "3 Months": "3mo",
    "6 Months": "6mo",
    "1 Year": "1y",
    "YTD": "ytd"
}

# --- FUNCTIONS ---

@st.cache_data(ttl=300) # Cache data for 5 minutes
def fetch_market_data(market_code, period_label):
    """
    Fetches batch data from yfinance and calculates returns.
    """
    stocks = STOCKS_DB[market_code]
    tickers = [s["ticker"] for s in stocks]
    yf_period = PERIOD_MAP[period_label]
    
    # Batch download is much faster than individual requests
    try:
        data = yf.download(tickers, period=yf_period, progress=False)['Close']
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

    # Calculate Percentage Change
    results = []
    
    if data.empty:
        return []

    # Get the last valid price
    current_prices = data.iloc[-1]
    
    # Get the start price based on period
    if period_label == "1 Day":
        # For 1 Day, we need previous close. 
        # yfinance '2d' usually gives us [Yesterday, Today]
        if len(data) >= 2:
            start_prices = data.iloc[-2]
        else:
            start_prices = data.iloc[0] # Fallback
    else:
        start_prices = data.iloc[0]

    for stock in stocks:
        ticker = stock["ticker"]
        if ticker in current_prices and ticker in start_prices:
            curr = current_prices[ticker]
            start = start_prices[ticker]
            
            # Avoid division by zero
            if pd.isna(curr) or pd.isna(start) or start == 0:
                change = 0.0
            else:
                change = ((curr - start) / start) * 100
                
            results.append({
                "Ticker": ticker.replace('.IS', '').replace('.L', ''),
                "Name": stock["name"],
                "Sector": stock["sector"],
                "Size": stock["mcap_weight"], # Used for box size
                "Change (%)": round(change, 2),
                "Price": round(curr, 2),
                "Label_Change": f"{round(change, 2)}%"
            })
            
    return results

def create_heatmap(df):
    """
    Creates the Treemap using Plotly Express
    """
    # Create custom color scale
    # Red for negative, Green for positive
    
    fig = px.treemap(
        df,
        path=[px.Constant("All Sectors"), 'Sector', 'Ticker'],
        values='Size',
        color='Change (%)',
        color_continuous_scale=['#d73027', '#f46d43', '#fee08b', '#d9ef8b', '#66bd63', '#1a9850'],
        color_continuous_midpoint=0,
        custom_data=['Name', 'Price', 'Change (%)'],
        hover_data={'Label_Change': True}
    )

    fig.update_traces(
        textposition="middle center",
        texttemplate="<b>%{label}</b><br>%{customdata[2]}%",
        hovertemplate='<b>%{customdata[0]}</b><br>Price: %{customdata[1]}<br>Change: %{customdata[2]}%<extra></extra>',
        marker=dict(line=dict(width=1, color='black')) # Borders
    )

    fig.update_layout(
        margin=dict(t=0, l=0, r=0, b=0),
        height=700,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial", size=14)
    )
    
    return fig

# --- MAIN APP LAYOUT ---

# Sidebar Controls
st.sidebar.title("⚙️ Controls")
selected_market = st.sidebar.radio("Select Market", ["TR", "UK"], index=0, format_func=lambda x: "🇹🇷 Borsa Istanbul" if x == "TR" else "🇬🇧 FTSE 100")
selected_period = st.sidebar.select_slider("Time Period", options=["1 Day", "5 Days", "1 Month", "3 Months", "6 Months", "1 Year", "YTD"], value="1 Day")

st.sidebar.markdown("---")
st.sidebar.title("👤 Account")

# Simulated Auth State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    with st.sidebar.form("login_form"):
        st.write("Sign in for Real-time Data")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            st.session_state.logged_in = True
            st.rerun()
    
    st.sidebar.info("💡 Pro Tip: Login to remove 15-min delay.")
else:
    st.sidebar.success(f"Welcome, Trader!")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# Main Content
st.title("MarketMap Pro 🚀")
st.markdown(f"### Heatmap: **{'BIST 100' if selected_market == 'TR' else 'FTSE 100'}** | Period: **{selected_period}**")

# Load Data
with st.spinner('Fetching live market data...'):
    data = fetch_market_data(selected_market, selected_period)
    
if data:
    df = pd.DataFrame(data)
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    avg_change = df["Change (%)"].mean()
    gainers = df[df["Change (%)"] > 0].shape[0]
    losers = df[df["Change (%)"] < 0].shape[0]
    top_stock = df.loc[df["Change (%)"].idxmax()]
    
    col1.metric("Market Sentiment", "Bullish" if avg_change > 0 else "Bearish", f"{avg_change:.2f}%")
    col2.metric("Gainers", gainers, delta_color="normal")
    col3.metric("Losers", losers, delta_color="inverse")
    col4.metric("Top Mover", top_stock['Ticker'], f"{top_stock['Change (%)']}%")

    # Render Heatmap
    fig = create_heatmap(df)
    st.plotly_chart(fig, use_container_width=True)

    # Data Table (Below Heatmap)
    with st.expander("View Raw Data"):
        st.dataframe(
            df.sort_values(by="Change (%)", ascending=False)
            .style.background_gradient(subset=["Change (%)"], cmap="RdYlGn", vmin=-5, vmax=5)
            .format({"Price": "{:.2f}", "Change (%)": "{:.2f}%"})
        )

else:
    st.error("Failed to load market data. Please check your connection or try again later.")
