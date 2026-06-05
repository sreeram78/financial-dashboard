"""
Financial Analytics Dashboard with Forecasting & Scenario Analysis
Built with Streamlit, Pandas, Plotly
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Financial Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .scenario-header {
        background: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .anomaly-high {
        background: #ffe6e6;
        padding: 10px;
        border-left: 4px solid #e74c3c;
        border-radius: 4px;
        margin: 5px 0;
    }
    .anomaly-medium {
        background: #fff5e6;
        padding: 10px;
        border-left: 4px solid #f39c12;
        border-radius: 4px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============= SESSION STATE INITIALIZATION =============
if 'df_pl' not in st.session_state:
    st.session_state.df_pl = None
if 'df_bs' not in st.session_state:
    st.session_state.df_bs = None
if 'df_cf' not in st.session_state:
    st.session_state.df_cf = None
if 'forecast_data' not in st.session_state:
    st.session_state.forecast_data = None

# ============= SAMPLE DATA =============
@st.cache_data
def load_sample_data():
    """Load sample financial data for demonstration"""
    years = ['2022', '2023', '2024', '2025', '2026']
    
    # P&L Data
    pl_data = {
        'Metric': ['Revenue', 'COGS', 'Gross Profit', 'Gross Margin %',
                   'OpEx', 'EBITDA', 'EBITDA Margin %', 'D&A',
                   'EBIT', 'Interest', 'EBT', 'Tax', 'Tax Rate %', 'Net Income', 'Net Margin %'],
        '2022': [450000, 180000, 270000, 60.0, 120000, 150000, 33.3, 30000,
                120000, 15000, 105000, 26250, 25.0, 78750, 17.5],
        '2023': [520000, 208000, 312000, 60.0, 135000, 177000, 34.0, 32000,
                145000, 14000, 131000, 32750, 25.0, 98250, 18.9],
        '2024': [645000, 258000, 387000, 60.0, 162000, 225000, 34.9, 35000,
                190000, 13000, 177000, 44250, 25.0, 132750, 20.6],
        '2025': [780000, 312000, 468000, 60.0, 195000, 273000, 35.0, 38000,
                235000, 12000, 223000, 55750, 25.0, 167250, 21.4],
        '2026': [950000, 380000, 570000, 60.0, 240000, 330000, 34.7, 42000,
                288000, 11000, 277000, 69250, 25.0, 207750, 21.9]
    }
    
    # Balance Sheet Data
    bs_data = {
        'Metric': ['Cash', 'AR', 'Inventory', 'Current Assets', 'PPE', 'Intangibles', 'Total Assets',
                   'AP', 'ST Debt', 'Current Liabilities', 'LT Debt', 'Total Debt', 'Total Liabilities', 
                   'Equity', 'Total L&E'],
        '2022': [50000, 75000, 45000, 170000, 200000, 80000, 450000,
                60000, 30000, 90000, 120000, 150000, 240000, 210000, 450000],
        '2023': [65000, 86667, 52000, 203667, 210000, 85000, 498667,
                65000, 30000, 95000, 110000, 140000, 235000, 263667, 498667],
        '2024': [85000, 107500, 64500, 257000, 225000, 95000, 577000,
                77000, 30000, 107000, 100000, 130000, 237000, 340000, 577000],
        '2025': [110000, 130000, 78000, 318000, 245000, 110000, 673000,
                93000, 30000, 123000, 90000, 120000, 243000, 430000, 673000],
        '2026': [145000, 158333, 95000, 398333, 270000, 130000, 798333,
                114000, 30000, 144000, 80000, 110000, 254000, 544333, 798333]
    }
    
    # Cash Flow Data
    cf_data = {
        'Metric': ['Operating CF', 'CapEx', 'Free CF', 'Debt Change', 'Equity Change', 'Cash Change', 'Ending Cash'],
        '2022': [95000, -25000, 70000, -10000, 20000, 80000, 50000],
        '2023': [120000, -30000, 90000, -10000, 53667, 133667, 65000],
        '2024': [155000, -35000, 120000, -10000, 76333, 186333, 85000],
        '2025': [190000, -40000, 150000, -10000, 90000, 230000, 110000],
        '2026': [235000, -50000, 185000, -10000, 114333, 289333, 145000]
    }
    
    df_pl = pd.DataFrame(pl_data)
    df_bs = pd.DataFrame(bs_data)
    df_cf = pd.DataFrame(cf_data)
    
    return df_pl, df_bs, df_cf

# ============= FORECASTING ENGINE =============
def generate_forecast(historical_revenue, historical_years, assumptions, forecast_years=3):
    """
    Generate multi-year forecast based on assumptions
    
    Parameters:
    - historical_revenue: list of historical revenues
    - assumptions: dict with revenue_growth, cogs_pct, opex_growth, capex_pct, tax_rate, debt_paydown
    - forecast_years: number of years to forecast
    """
    forecast = []
    last_year = int(historical_years[-1])
    last_revenue = historical_revenue[-1]
    last_debt = 110000  # From sample data
    last_equity = 544333  # From sample data
    last_cash = 145000  # From sample data
    last_da = 42000  # From sample data
    
    for i in range(1, forecast_years + 1):
        year = last_year + i
        
        # Revenue forecast
        revenue = last_revenue * ((1 + assumptions['revenue_growth'] / 100) ** i)
        
        # P&L components
        cogs = revenue * (assumptions['cogs_pct'] / 100)
        gross_profit = revenue - cogs
        gross_margin = (gross_profit / revenue) * 100
        
        # Operating expenses
        opex = 240000 * ((1 + assumptions['opex_growth'] / 100) ** i)
        ebitda = gross_profit - opex
        ebitda_margin = (ebitda / revenue) * 100
        
        # Depreciation & Amortization
        da = last_da + (1000 * (i - 1))
        ebit = ebitda - da
        
        # Interest (declining with debt paydown)
        debt = max(0, last_debt - (assumptions['debt_paydown'] * i))
        interest = debt * 0.08
        
        ebt = ebit - interest
        tax = ebt * (assumptions['tax_rate'] / 100)
        net_income = ebt - tax
        net_margin = (net_income / revenue) * 100
        
        # Cash Flow
        operating_cf = net_income + da - (revenue * 0.05)
        capex = revenue * (assumptions['capex_pct'] / 100)
        free_cf = operating_cf - capex
        
        # Balance Sheet
        equity = last_equity + net_income
        current_ratio = (revenue * 0.25) / (cogs * 0.15)  # Simplified
        debt_to_equity = debt / equity if equity > 0 else 0
        
        forecast.append({
            'Year': str(year),
            'Revenue': round(revenue, 0),
            'COGS': round(cogs, 0),
            'Gross_Profit': round(gross_profit, 0),
            'Gross_Margin': round(gross_margin, 1),
            'OpEx': round(opex, 0),
            'EBITDA': round(ebitda, 0),
            'EBITDA_Margin': round(ebitda_margin, 1),
            'D&A': round(da, 0),
            'EBIT': round(ebit, 0),
            'Interest': round(interest, 0),
            'EBT': round(ebt, 0),
            'Tax': round(tax, 0),
            'Net_Income': round(net_income, 0),
            'Net_Margin': round(net_margin, 1),
            'Operating_CF': round(operating_cf, 0),
            'CapEx': round(capex, 0),
            'Free_CF': round(free_cf, 0),
            'Debt': round(debt, 0),
            'Equity': round(equity, 0),
            'Current_Ratio': round(current_ratio, 2),
            'Debt_to_Equity': round(debt_to_equity, 2)
        })
    
    return pd.DataFrame(forecast)

# ============= SENSITIVITY ANALYSIS =============
def sensitivity_analysis(historical_revenue, historical_years, base_assumptions, variable, forecast_years=3):
    """Generate sensitivity analysis for a given variable"""
    
    ranges = {
        'revenue_growth': [5, 10, 15, 18, 20, 25, 30],
        'cogs_pct': [35, 37, 39, 40, 41, 43, 45],
        'opex_growth': [5, 8, 11, 12, 15, 18, 20],
        'capex_pct': [2, 3, 4, 5, 6, 7, 8],
        'tax_rate': [20, 22, 24, 25, 26, 28, 30],
        'debt_paydown': [0, 5000, 10000, 15000, 20000, 25000, 30000]
    }
    
    results = []
    for val in ranges[variable]:
        temp_assumptions = base_assumptions.copy()
        temp_assumptions[variable] = val
        
        temp_forecast = generate_forecast(historical_revenue, historical_years, temp_assumptions, forecast_years)
        
        # Get Year 3 values
        idx = min(2, len(temp_forecast) - 1)
        ni_y3 = temp_forecast.iloc[idx]['Net_Income']
        fcf_y3 = temp_forecast.iloc[idx]['Free_CF']
        
        base_forecast = generate_forecast(historical_revenue, historical_years, base_assumptions, forecast_years)
        base_ni = base_forecast.iloc[idx]['Net_Income']
        
        variance = ((ni_y3 - base_ni) / base_ni * 100) if base_ni != 0 else 0
        
        results.append({
            'Variable': val,
            'Net_Income': ni_y3,
            'Free_CF': fcf_y3,
            'Variance_Pct': variance
        })
    
    return pd.DataFrame(results)

# ============= MAIN APP =============
def main():
    # Header
    st.markdown("# 📊 Financial Intelligence Dashboard")
    st.markdown("### Advanced Analytics + Forecasting + Scenario Analysis")
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## Navigation")
        page = st.radio("Select View:", [
            "🏠 Landing Page",
            "📈 Forecasting & Scenarios",
            "📊 Sensitivity Analysis",
            "📋 P&L Analysis",
            "💼 Balance Sheet",
            "💰 Cash Flow",
            "📌 KPIs",
            "🔍 Transactions"
        ])
        
        st.markdown("---")
        st.markdown("## Data Upload")
        uploaded_file = st.file_uploader("Upload Excel/CSV file", type=['xlsx', 'csv'])
        
        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.xlsx'):
                    excel_file = pd.ExcelFile(uploaded_file)
                    st.session_state.df_pl = pd.read_excel(uploaded_file, sheet_name='P&L Statement')
                    st.session_state.df_bs = pd.read_excel(uploaded_file, sheet_name='Balance Sheet')
                    st.session_state.df_cf = pd.read_excel(uploaded_file, sheet_name='Cash Flow')
                    st.success("✅ Files uploaded successfully!")
                else:
                    st.session_state.df_pl = pd.read_csv(uploaded_file)
                    st.success("✅ CSV file uploaded successfully!")
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
        
        st.markdown("---")
        st.markdown("**Stakeholder View:**")
        stakeholder = st.selectbox("Select Stakeholder:", [
            "CFO / Finance Director",
            "Operations Finance",
            "Analyst / Investor Relations",
            "Board / Executive"
        ])
    
    # Load data
    if st.session_state.df_pl is None:
        df_pl, df_bs, df_cf = load_sample_data()
        st.session_state.df_pl = df_pl
        st.session_state.df_bs = df_bs
        st.session_state.df_cf = df_cf
        st.info("📌 Using sample data. Upload your own file in the sidebar to analyze your data.")
    else:
        df_pl = st.session_state.df_pl
        df_bs = st.session_state.df_bs
        df_cf = st.session_state.df_cf
    
    # ============= LANDING PAGE =============
    if page == "🏠 Landing Page":
        landing_page(df_pl, df_bs, df_cf, stakeholder)
    
    # ============= FORECASTING PAGE =============
    elif page == "📈 Forecasting & Scenarios":
        forecasting_page(df_pl, stakeholder)
    
    # ============= SENSITIVITY PAGE =============
    elif page == "📊 Sensitivity Analysis":
        sensitivity_page(df_pl)
    
    # ============= P&L PAGE =============
    elif page == "📈 P&L Analysis":
        pl_page(df_pl)
    
    # ============= BALANCE SHEET PAGE =============
    elif page == "💼 Balance Sheet":
        bs_page(df_bs)
    
    # ============= CASH FLOW PAGE =============
    elif page == "💰 Cash Flow":
        cf_page(df_cf)
    
    # ============= KPIs PAGE =============
    elif page == "📌 KPIs":
        kpi_page(df_pl, df_bs, df_cf)
    
    # ============= TRANSACTIONS PAGE =============
    elif page == "🔍 Transactions":
        transactions_page()

# ============= LANDING PAGE FUNCTION =============
def landing_page(df_pl, df_bs, df_cf, stakeholder):
    st.markdown("## Executive Summary")
    
    # Extract numeric columns
    numeric_cols = [col for col in df_pl.columns if col != 'Metric']
    
    # Calculate KPIs
    latest_idx = len(numeric_cols) - 1
    latest_year = numeric_cols[latest_idx]
    prev_year = numeric_cols[latest_idx - 1] if latest_idx > 0 else latest_year
    
    revenue_row = df_pl[df_pl['Metric'] == 'Revenue']
    ni_row = df_pl[df_pl['Metric'] == 'Net Income']
    
    if not revenue_row.empty and not ni_row.empty:
        latest_revenue = revenue_row[latest_year].values[0]
        prev_revenue = revenue_row[prev_year].values[0]
        latest_ni = ni_row[latest_year].values[0]
        
        yoy_growth = ((latest_revenue / prev_revenue) - 1) * 100
        ni_margin = (latest_ni / latest_revenue) * 100
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Revenue (Latest)", f"${latest_revenue/1000:.0f}M", f"{yoy_growth:.1f}% YoY")
        with col2:
            st.metric("Net Income Margin", f"{ni_margin:.1f}%", f"${latest_ni/1000:.0f}M")
        with col3:
            st.metric("Free Cash Flow", "$185M", "+18.0% YoY")
        with col4:
            st.metric("Debt/Equity Ratio", "0.19x", "↓ Improving")
    
    # Three Statements Summary
    st.markdown("---")
    st.markdown("## Financial Statements Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📊 Income Statement (2026)")
        revenue = df_pl[df_pl['Metric'] == 'Revenue'][latest_year].values[0]
        gross_profit = df_pl[df_pl['Metric'] == 'Gross Profit'][latest_year].values[0]
        ebitda = df_pl[df_pl['Metric'] == 'EBITDA'][latest_year].values[0]
        ni = df_pl[df_pl['Metric'] == 'Net Income'][latest_year].values[0]
        
        st.write(f"**Revenue:** ${revenue/1000:.0f}M")
        st.write(f"**Gross Profit:** ${gross_profit/1000:.0f}M")
        st.write(f"**EBITDA:** ${ebitda/1000:.0f}M")
        st.write(f"**Net Income:** ${ni/1000:.0f}M ✓")
    
    with col2:
        st.markdown("### 💼 Balance Sheet (2026)")
        if not df_bs.empty:
            cash = df_bs[df_bs['Metric'] == 'Cash'][latest_year].values[0] if 'Cash' in df_bs['Metric'].values else 145000
            assets = df_bs[df_bs['Metric'] == 'Total Assets'][latest_year].values[0] if 'Total Assets' in df_bs['Metric'].values else 798333
            debt = df_bs[df_bs['Metric'] == 'Total Debt'][latest_year].values[0] if 'Total Debt' in df_bs['Metric'].values else 110000
            equity = df_bs[df_bs['Metric'] == 'Equity'][latest_year].values[0] if 'Equity' in df_bs['Metric'].values else 544333
            
            st.write(f"**Cash:** ${cash/1000:.0f}M")
            st.write(f"**Total Assets:** ${assets/1000:.0f}M")
            st.write(f"**Total Debt:** ${debt/1000:.0f}M")
            st.write(f"**Equity:** ${equity/1000:.0f}M ✓")
    
    with col3:
        st.markdown("### 💰 Cash Flow (2026)")
        if not df_cf.empty:
            ocf = df_cf[df_cf['Metric'] == 'Operating CF'][latest_year].values[0] if 'Operating CF' in df_cf['Metric'].values else 235000
            capex = df_cf[df_cf['Metric'] == 'CapEx'][latest_year].values[0] if 'CapEx' in df_cf['Metric'].values else -50000
            fcf = df_cf[df_cf['Metric'] == 'Free CF'][latest_year].values[0] if 'Free CF' in df_cf['Metric'].values else 185000
            cash_pos = df_cf[df_cf['Metric'] == 'Ending Cash'][latest_year].values[0] if 'Ending Cash' in df_cf['Metric'].values else 145000
            
            st.write(f"**Operating CF:** ${ocf/1000:.0f}M")
            st.write(f"**CapEx:** ${capex/1000:.0f}M")
            st.write(f"**Free CF:** ${fcf/1000:.0f}M ✓")
            st.write(f"**Cash Position:** ${cash_pos/1000:.0f}M")
    
    # Quick navigation buttons
    st.markdown("---")
    st.markdown("## Explore Detailed Analysis")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📈 View Forecasts"):
            st.switch_page("pages/forecasting.py")
    with col2:
        if st.button("📊 Run Sensitivity"):
            st.switch_page("pages/sensitivity.py")
    with col3:
        if st.button("📋 View All KPIs"):
            st.switch_page("pages/kpis.py")

# ============= FORECASTING PAGE =============
def forecasting_page(df_pl, stakeholder):
    st.markdown("## 🔮 Financial Forecasting & Scenario Analysis")
    
    # Forecast period selector
    col1, col2, col3 = st.columns(3)
    
    with col1:
        forecast_years = st.selectbox("Forecast Period (Years):", [1, 2, 3, 5], index=2)
    
    with col2:
        scenario_choice = st.selectbox("Select Scenario:", [
            "Base Case (Most Likely)",
            "Bear Case (Conservative)",
            "Bull Case (Optimistic)",
            "Custom Scenario"
        ])
    
    # Scenario assumptions
    st.markdown("### 📋 Forecast Assumptions")
    
    # Default scenarios
    scenarios = {
        'Base Case (Most Likely)': {
            'revenue_growth': 18,
            'cogs_pct': 40,
            'opex_growth': 12,
            'capex_pct': 5,
            'tax_rate': 25,
            'debt_paydown': 10000
        },
        'Bear Case (Conservative)': {
            'revenue_growth': 10,
            'cogs_pct': 42,
            'opex_growth': 14,
            'capex_pct': 6,
            'tax_rate': 25,
            'debt_paydown': 5000
        },
        'Bull Case (Optimistic)': {
            'revenue_growth': 25,
            'cogs_pct': 38,
            'opex_growth': 10,
            'capex_pct': 4,
            'tax_rate': 25,
            'debt_paydown': 15000
        }
    }
    
    if scenario_choice != "Custom Scenario":
        assumptions = scenarios[scenario_choice]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Revenue Growth", f"{assumptions['revenue_growth']}%")
            st.metric("COGS %", f"{assumptions['cogs_pct']}%")
        with col2:
            st.metric("OpEx Growth", f"{assumptions['opex_growth']}%")
            st.metric("CapEx %", f"{assumptions['capex_pct']}%")
        with col3:
            st.metric("Tax Rate", f"{assumptions['tax_rate']}%")
            st.metric("Annual Debt Paydown", f"${assumptions['debt_paydown']/1000:.0f}M")
    else:
        # Custom scenario with sliders
        col1, col2, col3 = st.columns(3)
        
        with col1:
            assumptions = {}
            assumptions['revenue_growth'] = st.slider("Revenue Growth %", 0, 50, 18)
            assumptions['cogs_pct'] = st.slider("COGS %", 30, 50, 40)
        
        with col2:
            assumptions['opex_growth'] = st.slider("OpEx Growth %", 0, 30, 12)
            assumptions['capex_pct'] = st.slider("CapEx %", 2, 10, 5)
        
        with col3:
            assumptions['tax_rate'] = st.slider("Tax Rate %", 15, 35, 25)
            assumptions['debt_paydown'] = st.slider("Annual Debt Paydown ($M)", 0, 30, 10) * 1000
    
    # Generate forecast
    numeric_cols = [col for col in df_pl.columns if col != 'Metric']
    revenue_row = df_pl[df_pl['Metric'] == 'Revenue']
    
    if not revenue_row.empty:
        historical_revenue = revenue_row[numeric_cols].values[0].tolist()
        forecast_df = generate_forecast(historical_revenue, numeric_cols, assumptions, forecast_years)
        
        # Display forecast table
        st.markdown("### 📊 Forecast Results")
        
        # P&L Forecast
        st.markdown("#### Income Statement Forecast")
        pl_cols = ['Year', 'Revenue', 'COGS', 'Gross_Margin', 'EBITDA', 'EBITDA_Margin', 'Net_Income', 'Net_Margin']
        pl_display = forecast_df[pl_cols].copy()
        pl_display.columns = ['Year', 'Revenue ($)', 'COGS ($)', 'Gross Margin %', 'EBITDA ($)', 'EBITDA Margin %', 'Net Income ($)', 'Net Margin %']
        
        # Format for display
        for col in ['Revenue ($)', 'COGS ($)', 'EBITDA ($)', 'Net Income ($)']:
            pl_display[col] = pl_display[col].apply(lambda x: f"${x/1000:.0f}M")
        for col in ['Gross Margin %', 'EBITDA Margin %', 'Net Margin %']:
            pl_display[col] = pl_display[col].apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(pl_display, use_container_width=True)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Revenue & Net Income Trend")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=forecast_df['Year'],
                y=forecast_df['Revenue'],
                mode='lines+markers',
                name='Revenue',
                line=dict(color='#3498db', width=3)
            ))
            fig.add_trace(go.Scatter(
                x=forecast_df['Year'],
                y=forecast_df['Net_Income'],
                mode='lines+markers',
                name='Net Income',
                line=dict(color='#2ecc71', width=3)
            ))
            fig.update_layout(hovermode='x unified', height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Margin Trajectory")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=forecast_df['Year'],
                y=forecast_df['Gross_Margin'],
                mode='lines+markers',
                name='Gross Margin %',
                line=dict(color='#3498db')
            ))
            fig.add_trace(go.Scatter(
                x=forecast_df['Year'],
                y=forecast_df['EBITDA_Margin'],
                mode='lines+markers',
                name='EBITDA Margin %',
                line=dict(color='#f39c12')
            ))
            fig.add_trace(go.Scatter(
                x=forecast_df['Year'],
                y=forecast_df['Net_Margin'],
                mode='lines+markers',
                name='Net Margin %',
                line=dict(color='#2ecc71')
            ))
            fig.update_layout(hovermode='x unified', height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Balance Sheet Forecast
        st.markdown("#### Balance Sheet Forecast")
        bs_cols = ['Year', 'Debt', 'Equity', 'Debt_to_Equity', 'Current_Ratio']
        bs_display = forecast_df[bs_cols].copy()
        bs_display.columns = ['Year', 'Debt ($)', 'Equity ($)', 'Debt/Equity', 'Current Ratio']
        
        for col in ['Debt ($)', 'Equity ($)']:
            bs_display[col] = bs_display[col].apply(lambda x: f"${x/1000:.0f}M")
        for col in ['Debt/Equity', 'Current Ratio']:
            bs_display[col] = bs_display[col].apply(lambda x: f"{x:.2f}x")
        
        st.dataframe(bs_display, use_container_width=True)
        
        # Scenario comparison
        st.markdown("---")
        st.markdown("### 🔄 Scenario Comparison")
        
        # Generate all scenarios
        scenario_results = {}
        for scenario_name, scenario_assumptions in scenarios.items():
            scenario_forecast = generate_forecast(historical_revenue, numeric_cols, scenario_assumptions, forecast_years)
            scenario_results[scenario_name] = scenario_forecast.iloc[-1]  # Last year
        
        comparison_data = []
        for scenario_name, row in scenario_results.items():
            comparison_data.append({
                'Scenario': scenario_name.split('(')[0].strip(),
                'Revenue': f"${row['Revenue']/1000:.0f}M",
                'Net Income': f"${row['Net_Income']/1000:.0f}M",
                'Free CF': f"${row['Free_CF']/1000:.0f}M",
                'Debt/Equity': f"{row['Debt_to_Equity']:.2f}x"
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True)
        
        # Comparison chart
        fig = go.Figure(data=[
            go.Bar(name='Revenue', x=[s['Scenario'] for s in comparison_data], y=[float(s['Revenue'].replace('$', '').replace('M', '')) for s in comparison_data]),
            go.Bar(name='Net Income', x=[s['Scenario'] for s in comparison_data], y=[float(s['Net Income'].replace('$', '').replace('M', '')) for s in comparison_data]),
            go.Bar(name='Free CF', x=[s['Scenario'] for s in comparison_data], y=[float(s['Free CF'].replace('$', '').replace('M', '')) for s in comparison_data])
        ])
        fig.update_layout(barmode='group', height=400)
        st.plotly_chart(fig, use_container_width=True)

# ============= SENSITIVITY PAGE =============
def sensitivity_page(df_pl):
    st.markdown("## 📊 Sensitivity & What-If Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        forecast_years = st.selectbox("Forecast Period:", [1, 2, 3, 5], index=2)
    
    with col2:
        sensitivity_var = st.selectbox("Analyze Variable:", [
            'revenue_growth',
            'cogs_pct',
            'opex_growth',
            'capex_pct',
            'tax_rate',
            'debt_paydown'
        ], format_func=lambda x: {
            'revenue_growth': 'Revenue Growth %',
            'cogs_pct': 'COGS %',
            'opex_growth': 'OpEx Growth %',
            'capex_pct': 'CapEx %',
            'tax_rate': 'Tax Rate %',
            'debt_paydown': 'Debt Paydown'
        }[x])
    
    # Base assumptions
    base_assumptions = {
        'revenue_growth': 18,
        'cogs_pct': 40,
        'opex_growth': 12,
        'capex_pct': 5,
        'tax_rate': 25,
        'debt_paydown': 10000
    }
    
    # Get historical data
    numeric_cols = [col for col in df_pl.columns if col != 'Metric']
    revenue_row = df_pl[df_pl['Metric'] == 'Revenue']
    
    if not revenue_row.empty:
        historical_revenue = revenue_row[numeric_cols].values[0].tolist()
        
        # Run sensitivity
        sensitivity_df = sensitivity_analysis(historical_revenue, numeric_cols, base_assumptions, sensitivity_var, forecast_years)
        
        st.markdown("### Sensitivity Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Impact on Net Income")
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=sensitivity_df['Variable'],
                y=sensitivity_df['Net_Income'],
                name='Net Income',
                marker=dict(color='#2ecc71')
            ))
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Impact on Free Cash Flow")
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=sensitivity_df['Variable'],
                y=sensitivity_df['Free_CF'],
                name='Free CF',
                marker=dict(color='#f39c12')
            ))
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        # Sensitivity table
        st.markdown("### Detailed Sensitivity Table")
        display_df = sensitivity_df.copy()
        display_df.columns = ['Variable', 'Net Income ($)', 'Free CF ($)', 'Variance %']
        
        display_df['Net Income ($)'] = display_df['Net Income ($)'].apply(lambda x: f"${x/1000:.0f}M")
        display_df['Free CF ($)'] = display_df['Free CF ($)'].apply(lambda x: f"${x/1000:.0f}M")
        display_df['Variance %'] = display_df['Variance %'].apply(lambda x: f"{x:+.1f}%")
        
        st.dataframe(display_df, use_container_width=True)
        
        # Key insights
        st.markdown("---")
        st.markdown("### 💡 Key Insights")
        
        max_variance = sensitivity_df['Variance_Pct'].abs().max()
        min_ni = sensitivity_df['Net_Income'].min()
        max_ni = sensitivity_df['Net_Income'].max()
        
        st.write(f"""
        **Variable Impact Range:**
        - Minimum Net Income: ${min_ni/1000:.0f}M
        - Maximum Net Income: ${max_ni/1000:.0f}M
        - Variance Range: {max_variance:.1f}%
        
        **Key Finding:** Every 1% change in **{sensitivity_var.replace('_', ' ')}** 
        impacts Year {forecast_years} profitability by approximately **${(max_ni - min_ni) / len(sensitivity_df) / 1000:.0f}M**
        """)

# ============= P&L PAGE =============
def pl_page(df_pl):
    st.markdown("## 📈 Income Statement Analysis")
    
    # Display P&L table
    st.dataframe(df_pl, use_container_width=True)
    
    # Charts
    numeric_cols = [col for col in df_pl.columns if col != 'Metric']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Revenue & Net Income Trend")
        revenue = df_pl[df_pl['Metric'] == 'Revenue'][numeric_cols].values[0]
        ni = df_pl[df_pl['Metric'] == 'Net Income'][numeric_cols].values[0]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=numeric_cols, y=revenue, name='Revenue', marker=dict(color='#3498db')))
        fig.add_trace(go.Scatter(x=numeric_cols, y=ni, name='Net Income', yaxis='y2', line=dict(color='#2ecc71', width=3)))
        
        fig.update_layout(
            yaxis=dict(title='Revenue ($)'),
            yaxis2=dict(title='Net Income ($)', overlaying='y', side='right'),
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Margin Trends")
        gm = df_pl[df_pl['Metric'] == 'Gross Margin %'][numeric_cols].values[0]
        em = df_pl[df_pl['Metric'] == 'EBITDA Margin %'][numeric_cols].values[0]
        nm = df_pl[df_pl['Metric'] == 'Net Margin %'][numeric_cols].values[0]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=numeric_cols, y=gm, name='Gross Margin %', mode='lines+markers'))
        fig.add_trace(go.Scatter(x=numeric_cols, y=em, name='EBITDA Margin %', mode='lines+markers'))
        fig.add_trace(go.Scatter(x=numeric_cols, y=nm, name='Net Margin %', mode='lines+markers'))
        
        fig.update_layout(height=400, hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)

# ============= BALANCE SHEET PAGE =============
def bs_page(df_bs):
    st.markdown("## 💼 Balance Sheet Analysis")
    
    st.dataframe(df_bs, use_container_width=True)
    
    numeric_cols = [col for col in df_bs.columns if col != 'Metric']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Asset Composition")
        if 'Cash' in df_bs['Metric'].values:
            cash = df_bs[df_bs['Metric'] == 'Cash'][numeric_cols].values[0]
            fig = go.Figure(data=[go.Bar(x=numeric_cols, y=cash)])
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Debt vs Equity")
        if 'Total Debt' in df_bs['Metric'].values and 'Equity' in df_bs['Metric'].values:
            debt = df_bs[df_bs['Metric'] == 'Total Debt'][numeric_cols].values[0]
            equity = df_bs[df_bs['Metric'] == 'Equity'][numeric_cols].values[0]
            
            fig = go.Figure(data=[
                go.Bar(x=numeric_cols, y=debt, name='Debt'),
                go.Bar(x=numeric_cols, y=equity, name='Equity')
            ])
            fig.update_layout(barmode='stack', height=400)
            st.plotly_chart(fig, use_container_width=True)

# ============= CASH FLOW PAGE =============
def cf_page(df_cf):
    st.markdown("## 💰 Cash Flow Analysis")
    
    st.dataframe(df_cf, use_container_width=True)
    
    numeric_cols = [col for col in df_cf.columns if col != 'Metric']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Cash Flow Sources")
        if 'Operating CF' in df_cf['Metric'].values and 'Free CF' in df_cf['Metric'].values:
            ocf = df_cf[df_cf['Metric'] == 'Operating CF'][numeric_cols].values[0]
            fcf = df_cf[df_cf['Metric'] == 'Free CF'][numeric_cols].values[0]
            
            fig = go.Figure(data=[
                go.Bar(x=numeric_cols, y=ocf, name='Operating CF'),
                go.Bar(x=numeric_cols, y=fcf, name='Free CF')
            ])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Cash Position Trend")
        if 'Ending Cash' in df_cf['Metric'].values:
            cash = df_cf[df_cf['Metric'] == 'Ending Cash'][numeric_cols].values[0]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=numeric_cols, y=cash, mode='lines+markers', fill='tozeroy', name='Cash'))
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

# ============= KPI PAGE =============
def kpi_page(df_pl, df_bs, df_cf):
    st.markdown("## 📌 Key Performance Indicators")
    
    numeric_cols = [col for col in df_pl.columns if col != 'Metric']
    latest = numeric_cols[-1]
    
    # Profitability KPIs
    st.markdown("### 📊 Profitability KPIs")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        gm = df_pl[df_pl['Metric'] == 'Gross Margin %'][latest].values[0]
        st.metric("Gross Margin", f"{gm:.1f}%")
    with col2:
        em = df_pl[df_pl['Metric'] == 'EBITDA Margin %'][latest].values[0]
        st.metric("EBITDA Margin", f"{em:.1f}%")
    with col3:
        nm = df_pl[df_pl['Metric'] == 'Net Margin %'][latest].values[0]
        st.metric("Net Margin", f"{nm:.1f}%")
    with col4:
        revenue = df_pl[df_pl['Metric'] == 'Revenue'][latest].values[0]
        ni = df_pl[df_pl['Metric'] == 'Net Income'][latest].values[0]
        roe = (ni / 544333) * 100  # Approximate equity
        st.metric("ROE", f"{roe:.1f}%")
    
    # Liquidity KPIs
    st.markdown("---")
    st.markdown("### 💧 Liquidity & Solvency KPIs")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Current Ratio
        st.metric("Current Ratio", "1.6x", "✓ Healthy")
    with col2:
        # Quick Ratio
        st.metric("Quick Ratio", "1.4x", "✓ Strong")
    with col3:
        # Debt/Equity
        st.metric("Debt/Equity", "0.19x", "↓ Improving")
    with col4:
        # Interest Coverage
        st.metric("Interest Coverage", "26.2x", "✓ Excellent")
    
    # Efficiency KPIs
    st.markdown("---")
    st.markdown("### ⚙️ Efficiency KPIs")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Asset Turnover", "1.19x")
    with col2:
        st.metric("Inventory Turnover", "4.0x")
    with col3:
        st.metric("Days Payable", "109 days")
    
    # Growth KPIs
    st.markdown("---")
    st.markdown("### 📈 Growth KPIs")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        prev = numeric_cols[-2]
        revenue_prev = df_pl[df_pl['Metric'] == 'Revenue'][prev].values[0]
        revenue_latest = df_pl[df_pl['Metric'] == 'Revenue'][latest].values[0]
        growth = ((revenue_latest / revenue_prev) - 1) * 100
        st.metric("Revenue Growth", f"{growth:.1f}%")
    with col2:
        st.metric("5-Year CAGR", "20.8%")
    with col3:
        st.metric("EBITDA Growth", "18.1%")

# ============= TRANSACTIONS PAGE =============
def transactions_page():
    st.markdown("## 🔍 Transaction Details & Anomaly Detection")
    
    # Sample transactions
    transactions = pd.DataFrame({
        'Date': ['2026-01-15', '2026-01-16', '2026-01-17', '2026-01-18', '2026-01-19',
                '2026-01-20', '2026-01-21', '2026-01-22', '2026-01-23', '2026-01-24'],
        'Account': ['4100', '5100', '5200', '6100', '4100', '6200', '6300', '6400', '7100', '4100'],
        'Description': ['Product Sales', 'Raw Materials', 'Manufacturing Labor', 'Sales Commission',
                       'Product Sales', 'Marketing Campaign', 'R&D Software Dev', 'Office Rent',
                       'Depreciation', 'Product Sales'],
        'Category': ['Revenue', 'COGS', 'COGS', 'S&M', 'Revenue', 'S&M', 'R&D', 'G&A', 'D&A', 'Revenue'],
        'Amount': [125000, 35000, 28000, 8500, 98000, 15000, 22000, 45000, 12000, 155000],
        'Anomaly': ['', '', '', 'ANOMALY', '', '', '', '', '', '']
    })
    
    st.dataframe(transactions, use_container_width=True)
    
    # Anomaly section
    st.markdown("---")
    st.markdown("### ⚠️ Flagged Anomalies")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="anomaly-high"><strong>HIGH SEVERITY</strong><br/>Unusual Transaction (2026-01-18)<br/>Sales Commission: $8.5K<br/>→ Requires review</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="anomaly-medium"><strong>MEDIUM SEVERITY</strong><br/>High Revenue Variance<br/>Actual vs Forecast: +12%<br/>→ Monitor in next period</div>', unsafe_allow_html=True)

# ============= RUN APP =============
if __name__ == "__main__":
    main()
