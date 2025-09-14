# Marketing Intelligence Dashboard
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    layout="wide",
    page_title="Marketing Intelligence Dashboard",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# Simple CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 1.5rem 0 1rem 0;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3498db;
        margin: 0.5rem 0;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3498db;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">📊 Marketing Intelligence Dashboard</h1>', unsafe_allow_html=True)
st.markdown("**Connect marketing activity with business outcomes** - Upload your CSV files or use sample data")

# Data Loading Section
st.sidebar.header("📁 Data Sources")

# Option to use sample data or upload files
use_sample = st.sidebar.checkbox("Use sample data", value=True)

uploaded_files = {}
if not use_sample:
    st.sidebar.info("Upload your CSV files:")
    uploaded_files['facebook'] = st.sidebar.file_uploader("Facebook.csv", type=["csv"])
    uploaded_files['google'] = st.sidebar.file_uploader("Google.csv", type=["csv"])
    uploaded_files['tiktok'] = st.sidebar.file_uploader("TikTok.csv", type=["csv"])
    uploaded_files['business'] = st.sidebar.file_uploader("Business.csv", type=["csv"])

# Data Processing Functions
def load_and_process_data(use_sample_data=True, uploaded_files=None):
    """Load and process marketing and business data"""
    try:
        if use_sample_data:
            # Load sample data
            fb_df = pd.read_csv("data/Facebook.csv")
            gg_df = pd.read_csv("data/Google.csv")
            tt_df = pd.read_csv("data/TikTok.csv")
            biz_df = pd.read_csv("data/Business.csv")
        else:
            # Load uploaded data
            if not all(uploaded_files.values()):
                st.error("Please upload all 4 CSV files or use sample data")
                return None, None
            
            fb_df = pd.read_csv(uploaded_files['facebook'])
            gg_df = pd.read_csv(uploaded_files['google'])
            tt_df = pd.read_csv(uploaded_files['tiktok'])
            biz_df = pd.read_csv(uploaded_files['business'])
        
        # Add channel column to marketing data
        fb_df['channel'] = 'Facebook'
        gg_df['channel'] = 'Google'
        tt_df['channel'] = 'TikTok'
        
        # Combine marketing data
        marketing_df = pd.concat([fb_df, gg_df, tt_df], ignore_index=True)
        
        # Convert date columns - handle multiple date formats
        marketing_df['date'] = pd.to_datetime(marketing_df['date'], errors='coerce')
        biz_df['date'] = pd.to_datetime(biz_df['date'], errors='coerce')
        
        # If parsing failed, try alternative formats
        if marketing_df['date'].isna().any():
            marketing_df['date'] = pd.to_datetime(marketing_df['date'], format='%d-%m-%Y', errors='coerce')
        if biz_df['date'].isna().any():
            biz_df['date'] = pd.to_datetime(biz_df['date'], format='%Y-%m-%d', errors='coerce')
        
        # Clean and fill missing values (but preserve date columns)
        marketing_df = marketing_df.fillna(0)
        biz_df = biz_df.fillna(0)
        
        # Debug: Check date parsing results
        if marketing_df['date'].isna().all():
            st.warning("Warning: Could not parse dates in marketing data. Please check date format.")
        if biz_df['date'].isna().all():
            st.warning("Warning: Could not parse dates in business data. Please check date format.")
        
        return marketing_df, biz_df
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None

def calculate_metrics(marketing_df, biz_df):
    """Calculate key marketing and business metrics"""
    # Marketing metrics
    total_spend = marketing_df['spend'].sum()
    total_impressions = marketing_df['impression'].sum()
    total_clicks = marketing_df['clicks'].sum()
    total_attributed_revenue = marketing_df['attributed revenue'].sum()
    
    # Business metrics
    total_orders = biz_df['# of orders'].sum()
    total_revenue = biz_df['total revenue'].sum()
    total_profit = biz_df['gross profit'].sum()
    new_customers = biz_df['new customers'].sum()
    
    # Calculated metrics
    roas = total_attributed_revenue / total_spend if total_spend > 0 else 0
    ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    cpc = total_spend / total_clicks if total_clicks > 0 else 0
    conversion_rate = (total_orders / total_clicks * 100) if total_clicks > 0 else 0
    profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
    
    return {
        'total_spend': total_spend,
        'total_impressions': total_impressions,
        'total_clicks': total_clicks,
        'total_attributed_revenue': total_attributed_revenue,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_profit': total_profit,
        'new_customers': new_customers,
        'roas': roas,
        'ctr': ctr,
        'cpc': cpc,
        'conversion_rate': conversion_rate,
        'profit_margin': profit_margin
    }

# Load data
marketing_df, biz_df = load_and_process_data(use_sample, uploaded_files)

if marketing_df is None or biz_df is None:
    st.stop()

# Show data info
st.sidebar.success(f"✅ Marketing data: {len(marketing_df)} rows")
st.sidebar.success(f"✅ Business data: {len(biz_df)} rows")
st.sidebar.info(f"📅 Date range: {marketing_df['date'].min().strftime('%Y-%m-%d')} to {marketing_df['date'].max().strftime('%Y-%m-%d')}")

# Sidebar Filters
st.sidebar.header("🔍 Filters")

# Date range filter
min_date = marketing_df['date'].min()
max_date = marketing_df['date'].max()

# Ensure dates are datetime objects
if pd.isna(min_date) or pd.isna(max_date):
    st.error("No valid dates found in the data. Please check your CSV files.")
    st.stop()

# Convert to date objects for the date input widget
min_date_obj = min_date.date() if hasattr(min_date, 'date') else pd.to_datetime(min_date).date()
max_date_obj = max_date.date() if hasattr(max_date, 'date') else pd.to_datetime(max_date).date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=[min_date_obj, max_date_obj],
    min_value=min_date_obj,
    max_value=max_date_obj
)

# Channel filter
channels = st.sidebar.multiselect(
    "Channels",
    options=sorted(marketing_df['channel'].unique()),
    default=sorted(marketing_df['channel'].unique())
)

# State filter (if available)
if 'state' in marketing_df.columns:
    states = st.sidebar.multiselect(
        "States",
        options=sorted(marketing_df['state'].dropna().unique()),
        default=sorted(marketing_df['state'].dropna().unique())
    )
else:
    states = None

# Apply filters
start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

filtered_marketing = marketing_df[
    (marketing_df['date'] >= start_date) & 
    (marketing_df['date'] <= end_date) &
    (marketing_df['channel'].isin(channels))
].copy()

if states:
    filtered_marketing = filtered_marketing[filtered_marketing['state'].isin(states)]

filtered_business = biz_df[
    (biz_df['date'] >= start_date) & 
    (biz_df['date'] <= end_date)
].copy()

if filtered_marketing.empty:
    st.warning("No data available for the selected filters")
    st.stop()

# Calculate metrics
metrics = calculate_metrics(filtered_marketing, filtered_business)

# Data Sources Info
st.markdown('<h2 class="sub-header">📊 Data Sources</h2>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.info("**Marketing Data (Facebook, Google, TikTok):**\n- Spend, Impressions, Clicks\n- Attributed Revenue by Campaign")
with col2:
    st.info("**Business Data (Business.csv):**\n- Orders, New Customers\n- Total Revenue, Gross Profit\n- COGS (Cost of Goods Sold)")

# Key Performance Indicators
st.markdown('<h2 class="sub-header">📈 Key Performance Indicators</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Spend", f"${metrics['total_spend']:,.0f}")
    st.metric("ROAS", f"{metrics['roas']:.2f}")

with col2:
    st.metric("Attributed Revenue", f"${metrics['total_attributed_revenue']:,.0f}")
    st.metric("CTR", f"{metrics['ctr']:.2f}%")

with col3:
    st.metric("Total Orders", f"{metrics['total_orders']:,.0f}")
    st.metric("Conversion Rate", f"{metrics['conversion_rate']:.2f}%")

with col4:
    st.metric("New Customers", f"{metrics['new_customers']:,.0f}")
    st.metric("Profit Margin", f"{metrics['profit_margin']:.2f}%")

# Performance Trends
st.markdown('<h2 class="sub-header">📊 Performance Trends</h2>', unsafe_allow_html=True)

# Daily aggregation
daily_marketing = filtered_marketing.groupby('date').agg({
    'spend': 'sum',
    'attributed revenue': 'sum',
    'impression': 'sum',
    'clicks': 'sum'
}).reset_index()

daily_business = filtered_business.groupby('date').agg({
    '# of orders': 'sum',
    'total revenue': 'sum',
    'gross profit': 'sum',
    'new customers': 'sum'
}).reset_index()

# Merge daily data
daily_combined = pd.merge(daily_marketing, daily_business, on='date', how='outer').fillna(0)

# Create trend chart
fig_trends = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Spend vs Revenue', 'Orders & New Customers', 'ROAS Trend', 'Conversion Metrics'),
    specs=[[{"secondary_y": True}, {"secondary_y": True}],
           [{"secondary_y": True}, {"secondary_y": True}]]
)

# Spend vs Revenue
fig_trends.add_trace(
    go.Scatter(x=daily_combined['date'], y=daily_combined['spend'], 
               name='Spend', line=dict(color='red', width=2)),
    row=1, col=1, secondary_y=False
)
fig_trends.add_trace(
    go.Scatter(x=daily_combined['date'], y=daily_combined['attributed revenue'], 
               name='Attributed Revenue', line=dict(color='green', width=2)),
    row=1, col=1, secondary_y=True
)

# Orders & New Customers
fig_trends.add_trace(
    go.Scatter(x=daily_combined['date'], y=daily_combined['# of orders'], 
               name='Orders', line=dict(color='blue', width=2)),
    row=1, col=2, secondary_y=False
)
fig_trends.add_trace(
    go.Scatter(x=daily_combined['date'], y=daily_combined['new customers'], 
               name='New Customers', line=dict(color='orange', width=2)),
    row=1, col=2, secondary_y=True
)

# ROAS Trend
daily_combined['roas'] = daily_combined['attributed revenue'] / daily_combined['spend'].replace(0, np.nan)
fig_trends.add_trace(
    go.Scatter(x=daily_combined['date'], y=daily_combined['roas'], 
               name='ROAS', line=dict(color='purple', width=2)),
    row=2, col=1, secondary_y=False
)

# Conversion Metrics
daily_combined['ctr'] = (daily_combined['clicks'] / daily_combined['impression'] * 100).replace([np.inf, -np.inf], 0)
daily_combined['conversion_rate'] = (daily_combined['# of orders'] / daily_combined['clicks'] * 100).replace([np.inf, -np.inf], 0)
fig_trends.add_trace(
    go.Scatter(x=daily_combined['date'], y=daily_combined['ctr'], 
               name='CTR %', line=dict(color='brown', width=2)),
    row=2, col=2, secondary_y=False
)
fig_trends.add_trace(
    go.Scatter(x=daily_combined['date'], y=daily_combined['conversion_rate'], 
               name='Conversion Rate %', line=dict(color='pink', width=2)),
    row=2, col=2, secondary_y=True
)

fig_trends.update_layout(height=600, showlegend=True, title_text="Daily Performance Trends")
st.plotly_chart(fig_trends, use_container_width=True)

# Channel Performance Analysis
st.markdown('<h2 class="sub-header">🎯 Channel Performance Analysis</h2>', unsafe_allow_html=True)

channel_performance = filtered_marketing.groupby('channel').agg({
    'spend': 'sum',
    'attributed revenue': 'sum',
    'impression': 'sum',
    'clicks': 'sum'
}).reset_index()

channel_performance['roas'] = channel_performance['attributed revenue'] / channel_performance['spend']
channel_performance['ctr'] = (channel_performance['clicks'] / channel_performance['impression'] * 100).replace([np.inf, -np.inf], 0)

col1, col2 = st.columns(2)

with col1:
    # Spend vs Revenue by Channel
    fig_spend_rev = px.bar(
        channel_performance, 
        x='channel', 
        y=['spend', 'attributed revenue'],
        title='Spend vs Attributed Revenue by Channel',
        barmode='group'
    )
    fig_spend_rev.update_layout(height=400)
    st.plotly_chart(fig_spend_rev, use_container_width=True)

with col2:
    # ROAS by Channel
    fig_roas = px.bar(
        channel_performance, 
        x='channel', 
        y='roas',
        title='ROAS by Channel',
        color='roas',
        color_continuous_scale='RdYlGn'
    )
    fig_roas.update_layout(height=400)
    st.plotly_chart(fig_roas, use_container_width=True)

# Campaign Performance
st.markdown('<h2 class="sub-header">🚀 Top Campaign Performance</h2>', unsafe_allow_html=True)

campaign_performance = filtered_marketing.groupby(['campaign', 'channel']).agg({
    'spend': 'sum',
    'attributed revenue': 'sum',
    'impression': 'sum',
    'clicks': 'sum'
}).reset_index()

campaign_performance['roas'] = campaign_performance['attributed revenue'] / campaign_performance['spend']
campaign_performance['ctr'] = (campaign_performance['clicks'] / campaign_performance['impression'] * 100).replace([np.inf, -np.inf], 0)

# Top 10 campaigns by ROAS
top_campaigns = campaign_performance.nlargest(10, 'roas')

st.dataframe(
    top_campaigns[['campaign', 'channel', 'spend', 'attributed revenue', 'roas', 'ctr']].round(2),
    use_container_width=True
)

# Business Insights
st.markdown('<h2 class="sub-header">💡 Business Insights</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    best_channel = channel_performance.loc[channel_performance['roas'].idxmax()]
    st.write(f"**Best Performing Channel:** {best_channel['channel']}")
    st.write(f"ROAS: {best_channel['roas']:.2f}")
    st.write(f"Spend: ${best_channel['spend']:,.0f}")
    st.write(f"Revenue: ${best_channel['attributed revenue']:,.0f}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    if metrics['roas'] > 3.0:
        st.success("🎉 **Excellent Performance!** ROAS above 3.0 indicates strong marketing efficiency")
    elif metrics['roas'] > 2.0:
        st.info("✅ **Good Performance** ROAS above 2.0 shows positive returns")
    else:
        st.warning("⚠️ **Needs Attention** ROAS below 2.0 - consider optimizing campaigns")
    
    if metrics['conversion_rate'] > 2.0:
        st.success("High conversion rate indicates effective targeting")
    else:
        st.info("Consider improving conversion rate through better targeting")
    st.markdown('</div>', unsafe_allow_html=True)

# Business Performance Analysis (from Business.csv)
st.markdown('<h2 class="sub-header">💼 Business Performance Analysis</h2>', unsafe_allow_html=True)

# Show business metrics from Business.csv
business_summary = filtered_business.groupby('date').agg({
    '# of orders': 'sum',
    'new customers': 'sum', 
    'total revenue': 'sum',
    'gross profit': 'sum'
}).reset_index()

col1, col2 = st.columns(2)

with col1:
    # Orders vs New Customers
    fig_orders = go.Figure()
    fig_orders.add_trace(go.Scatter(x=business_summary['date'], y=business_summary['# of orders'], 
                                   name='Total Orders', line=dict(color='blue', width=2)))
    fig_orders.add_trace(go.Scatter(x=business_summary['date'], y=business_summary['new customers'], 
                                   name='New Customers', line=dict(color='green', width=2)))
    fig_orders.update_layout(title='Orders vs New Customers (from Business.csv)', height=400)
    st.plotly_chart(fig_orders, use_container_width=True)

with col2:
    # Revenue vs Profit
    fig_revenue = go.Figure()
    fig_revenue.add_trace(go.Scatter(x=business_summary['date'], y=business_summary['total revenue'], 
                                    name='Total Revenue', line=dict(color='purple', width=2)))
    fig_revenue.add_trace(go.Scatter(x=business_summary['date'], y=business_summary['gross profit'], 
                                    name='Gross Profit', line=dict(color='orange', width=2)))
    fig_revenue.update_layout(title='Revenue vs Profit (from Business.csv)', height=400)
    st.plotly_chart(fig_revenue, use_container_width=True)

# Marketing Funnel Analysis
st.markdown('<h2 class="sub-header">🔄 Marketing Funnel Analysis</h2>', unsafe_allow_html=True)

funnel_data = {
    'Stage': ['Impressions', 'Clicks', 'Orders', 'Revenue'],
    'Value': [metrics['total_impressions'], metrics['total_clicks'], metrics['total_orders'], metrics['total_attributed_revenue']]
}

fig_funnel = px.funnel(
    funnel_data, 
    x='Value', 
    y='Stage',
    title='Marketing Funnel Performance'
)
fig_funnel.update_layout(height=400)
st.plotly_chart(fig_funnel, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**Marketing Intelligence Dashboard** - Built with Streamlit | Data-driven marketing insights")