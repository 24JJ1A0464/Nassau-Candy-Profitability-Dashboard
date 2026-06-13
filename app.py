import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- 1. Page Configuration ---
st.set_page_config(page_title="Profitability Dashboard", layout="wide")
st.title("Candy Distribution & Profitability Dashboard")

# --- 2. Data Loading ---
@st.cache_data
def load_data():
    # Attempt to load the real CSV, fallback to generated dummy data mimicking your Excel sheet
    try:
        df = pd.read_csv("Nassau Candy Distributor (1).csv")
        # Ensure dates are parsed correctly
        if 'Order Date' in df.columns:
            df['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed', dayfirst=True)
    except FileNotFoundError:
        # Fallback dummy data for immediate testing
        np.random.seed(42)
        products = ['Wonka Bar - Milk Chocolate', 'Everlasting Gobstopper', 'Fun Dip', 
                    'Kazookles', 'Lickable Wallpaper', 'Scrumdiddlyumptious', 'Nerds']
        divisions = ['Chocolate', 'Sugar', 'Other']
        
        data = []
        for i in range(200):
            sales = np.random.uniform(50, 5000)
            margin_pct = np.random.uniform(0.05, 0.95)
            cost = sales * (1 - margin_pct)
            data.append({
                'Order Date': pd.Timestamp('2026-01-01') + pd.Timedelta(days=np.random.randint(0, 180)),
                'Division': np.random.choice(divisions),
                'Product Name': np.random.choice(products),
                'Sales': sales,
                'Cost': cost,
                'Gross Profit': sales - cost,
                'Units': np.random.randint(1, 100)
            })
        df = pd.DataFrame(data)
        df['Gross Margin (%)'] = df['Gross Profit'] / df['Sales']
        
    return df

df = load_data()

# --- 3. Sidebar: User Capabilities ---
st.sidebar.header("Filters & Controls")

# Date Range Selector
min_date = df['Order Date'].min().date() if 'Order Date' in df.columns else None
max_date = df['Order Date'].max().date() if 'Order Date' in df.columns else None
if min_date and max_date:
    start_date, end_date = st.sidebar.date_input("Select Date Range", [min_date, max_date])
    df = df[(df['Order Date'].dt.date >= start_date) & (df['Order Date'].dt.date <= end_date)]

# Division Filter
divisions = df['Division'].unique().tolist() if 'Division' in df.columns else []
selected_divisions = st.sidebar.multiselect("Filter by Division", divisions, default=divisions)
if selected_divisions:
    df = df[df['Division'].isin(selected_divisions)]

# Product Search
search_query = st.sidebar.text_input("Search Product Name")
if search_query:
    df = df[df['Product Name'].str.contains(search_query, case=False, na=False)]

# Margin Threshold Slider
margin_threshold = st.sidebar.slider("Margin Risk Threshold (%)", min_value=0.0, max_value=1.0, value=0.15, step=0.01)

# --- 4. Data Aggregation ---
# Aggregate to Product Level
prod_df = df.groupby('Product Name').agg(
    Sales=('Sales', 'sum'),
    Cost=('Cost', 'sum'),
    Gross_Profit=('Gross Profit', 'sum'),
    Units=('Units', 'sum')
).reset_index()
prod_df['Gross_Margin'] = prod_df['Gross_Profit'] / prod_df['Sales']

# Sort for Pareto
prod_df = prod_df.sort_values(by='Gross_Profit', ascending=False)
prod_df['Cumulative_Profit'] = prod_df['Gross_Profit'].cumsum()
prod_df['Cumulative_Percentage'] = prod_df['Cumulative_Profit'] / prod_df['Gross_Profit'].sum()

# --- 5. Dashboard Modules ---

tab1, tab2, tab3 = st.tabs(["Profitability & Concentration", "Cost Diagnostics", "Division Performance"])

with tab1:
    st.header("Profit Concentration Analysis")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Pareto Chart
        fig_pareto = go.Figure()
        fig_pareto.add_trace(go.Bar(
            x=prod_df['Product Name'], y=prod_df['Gross_Profit'], name="Gross Profit", marker_color='#1f77b4'
        ))
        fig_pareto.add_trace(go.Scatter(
            x=prod_df['Product Name'], y=prod_df['Cumulative_Percentage'], name="Cumulative %", 
            yaxis='y2', mode='lines+markers', line=dict(color='#d62728', width=3)
        ))
        fig_pareto.update_layout(
            title="80/20 Profit Pareto Chart",
            yaxis=dict(title="Gross Profit ($)"),
            yaxis2=dict(title="Cumulative %", overlaying='y', side='right', tickformat='.0%'),
            hovermode="x unified",
            height=500
        )
        # 80% Threshold Line
        fig_pareto.add_hline(y=0.80, line_dash="dash", line_color="green", yref="y2", annotation_text="80% Threshold")
        st.plotly_chart(fig_pareto, use_container_width=True)

    with col2:
        # Product Margin Leaderboard
        st.subheader("Top Profit Contributors")
        st.dataframe(
            prod_df[['Product Name', 'Gross_Profit', 'Gross_Margin']].head(10).style.format({
                'Gross_Profit': '${:,.2f}',
                'Gross_Margin': '{:.2%}'
            }),
            hide_index=True, use_container_width=True
        )

with tab2:
    st.header("Cost vs Margin Diagnostics")
    
    # Flag Products based on slider
    prod_df['Risk_Flag'] = np.where(prod_df['Gross_Margin'] < margin_threshold, 'High Risk (Discontinue/Reprice)', 'Healthy')
    
    # Cost-Sales Scatter Plot
    fig_scatter = px.scatter(
        prod_df, x="Cost", y="Sales", color="Risk_Flag",
        size="Gross_Profit", hover_name="Product Name",
        title="Cost vs Sales (Bubble size = Profit)",
        color_discrete_map={"Healthy": "#2ca02c", "High Risk (Discontinue/Reprice)": "#d62728"},
        height=600
    )
    # Add quadrant lines
    fig_scatter.add_vline(x=prod_df['Cost'].mean(), line_dash="dot", line_color="gray", opacity=0.5)
    fig_scatter.add_hline(y=prod_df['Sales'].mean(), line_dash="dot", line_color="gray", opacity=0.5)
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab3:
    st.header("Division Performance Dashboard")
    if 'Division' in df.columns:
        div_df = df.groupby('Division').agg(
            Sales=('Sales', 'sum'),
            Gross_Profit=('Gross Profit', 'sum')
        ).reset_index()
        div_df['Margin'] = div_df['Gross_Profit'] / div_df['Sales']
        
        col_div1, col_div2 = st.columns(2)
        
        with col_div1:
            # Revenue vs Profit Comparison
            fig_div_bar = go.Figure()
            fig_div_bar.add_trace(go.Bar(x=div_df['Division'], y=div_df['Sales'], name='Revenue'))
            fig_div_bar.add_trace(go.Bar(x=div_df['Division'], y=div_df['Gross_Profit'], name='Profit'))
            fig_div_bar.update_layout(barmode='group', title="Revenue vs Profit by Division", height=450)
            st.plotly_chart(fig_div_bar, use_container_width=True)
            
        with col_div2:
            # Margin Distribution
            fig_div_margin = px.bar(
                div_df, x='Division', y='Margin', text='Margin',
                title="Average Margin by Division", color='Margin', color_continuous_scale='Blues', height=450
            )
            fig_div_margin.update_traces(texttemplate='%{text:.2%}', textposition='outside')
            fig_div_margin.update_layout(yaxis_tickformat='.0%')
            st.plotly_chart(fig_div_margin, use_container_width=True)
    else:
        st.warning("Division data not found in the dataset.")