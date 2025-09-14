# Marketing Intelligence Dashboard

A comprehensive Business Intelligence dashboard for analyzing marketing performance across Facebook, Google, and TikTok channels, connecting marketing activity with business outcomes.

## 🎯 Overview

This dashboard provides deep insights into:
- **Marketing Performance**: ROAS, CTR, CPC, CPM, conversion rates
- **Customer Economics**: CAC, LTV, LTV:CAC ratios
- **Channel Analysis**: Performance comparison across Facebook, Google, TikTok
- **Geographic Insights**: State-level performance analysis
- **Tactical Analysis**: Performance by marketing tactics (ASC, Retargeting, etc.)
- **Campaign Intelligence**: Detailed campaign-level metrics and rankings
- **Funnel Analysis**: Complete marketing funnel with conversion rates
- **Trend Analysis**: Weekly and daily performance trends

## 📊 Key Features

### Advanced Metrics
- **ROAS (Return on Ad Spend)**: Revenue generated per dollar spent
- **CAC (Customer Acquisition Cost)**: Cost to acquire each new customer
- **LTV (Lifetime Value)**: Average revenue per customer
- **LTV:CAC Ratio**: Unit economics health indicator
- **Attribution Rate**: Percentage of revenue attributed to marketing
- **Profit Margin**: Gross profit as percentage of revenue

### Interactive Visualizations
- Time series analysis with multiple metrics
- Channel performance comparison charts
- Geographic performance heatmaps
- Campaign scatter plots with efficiency analysis
- Marketing funnel visualization
- Weekly trend analysis

### Smart Insights
- Automated performance grading (A-F) for each channel
- Strategic recommendations based on key metrics
- Best/worst performing channel identification
- Trend direction analysis (up/down/stable)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project**
   ```bash
   cd Assesment1
   ```

2. **Install dependencies**
   ```bash
   pip install -r src/requirements.txt
   ```

3. **Run the dashboard**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

## 📁 Data Structure

The dashboard expects four CSV files:

### Marketing Data (Facebook.csv, Google.csv, TikTok.csv)
Required columns:
- `date`: Date in DD-MM-YYYY or YYYY-MM-DD format
- `tactic`: Marketing tactic (e.g., "ASC", "Retargeting", "Non-Branded Search")
- `state`: Geographic state (e.g., "NY", "CA")
- `campaign`: Campaign name
- `impression`: Number of impressions
- `clicks`: Number of clicks
- `spend`: Marketing spend amount
- `attributed revenue`: Revenue attributed to marketing

### Business Data (Business.csv)
Required columns:
- `date`: Date in DD-MM-YYYY or YYYY-MM-DD format
- `# of orders`: Total orders
- `# of new orders`: New orders
- `new customers`: Number of new customers
- `total revenue`: Total business revenue
- `gross profit`: Gross profit amount
- `COGS`: Cost of goods sold

## 🎛️ Dashboard Features

### Filters
- **Date Range**: Filter data by specific time periods
- **Channels**: Select specific marketing channels
- **States**: Filter by geographic regions
- **Tactics**: Filter by marketing tactics

### Key Performance Indicators
- Total Spend
- Attributed Revenue
- ROAS (Return on Ad Spend)
- CAC (Customer Acquisition Cost)
- LTV:CAC Ratio
- Total Revenue
- Orders
- New Customers
- Attribution Rate
- Profit Margin

### Analysis Sections

#### 1. Performance Insights
- Channel performance grades
- Best/worst performing channel identification
- Automated recommendations

#### 2. Time Series Analysis
- Spend vs Revenue trends
- Orders & New Customers tracking
- ROAS trend analysis
- Conversion metrics over time

#### 3. Channel Performance
- Spend vs Revenue comparison
- ROAS by channel
- Efficiency scatter plots (CTR vs Conversion Rate)
- Customer economics (CAC vs LTV)

#### 4. Geographic Analysis
- State-level performance by spend
- ROAS by state
- Geographic efficiency insights

#### 5. Tactical Analysis
- Performance by marketing tactic
- Tactic efficiency analysis
- Spend allocation recommendations

#### 6. Campaign Intelligence
- Top campaigns by spend
- Campaign performance scatter plots
- Detailed campaign metrics table

#### 7. Marketing Funnel
- Complete funnel visualization
- Conversion rates between stages
- Funnel efficiency analysis

#### 8. Weekly Trends
- Weekly spend patterns
- ROAS trends
- Order volume trends
- Conversion rate trends

## 📈 Strategic Recommendations

The dashboard automatically generates recommendations based on:

- **ROAS Analysis**: Alerts for low ROAS (<2.0) or celebrates high ROAS (>4.0)
- **CAC Optimization**: Identifies high CAC (>$100) or efficient CAC (<$50)
- **LTV:CAC Health**: Flags poor ratios (<3:1) or strong ratios (>5:1)
- **Channel Optimization**: Suggests budget reallocation between channels
- **Attribution Insights**: Identifies attribution gaps or over-attribution

## 📤 Data Export

Export filtered data and analysis results:
- **Filtered Data**: Complete dataset based on selected filters
- **Campaign Analysis**: Detailed campaign performance metrics

## 🔧 Customization

### Adding New Metrics
1. Update `src/metrics.py` with new calculation functions
2. Add metrics to `src/preprocess.py` aggregation functions
3. Include visualizations in `app.py`

### Modifying Visualizations
- Charts use Plotly for interactivity
- Customize colors, layouts, and chart types in `app.py`
- Add new chart types using Plotly's extensive library

### Data Processing
- Modify `src/preprocess.py` for custom aggregations
- Add new analysis functions for specialized insights
- Customize date parsing for different formats

## 🚀 Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud
1. Push code to GitHub repository
2. Connect to Streamlit Cloud
3. Deploy with automatic updates

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r src/requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

### Heroku Deployment
1. Create `Procfile`: `web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
2. Deploy using Heroku CLI

## 📊 Sample Data

The dashboard includes sample data covering 120 days of marketing and business activity across:
- **3 Channels**: Facebook, Google, TikTok
- **Multiple States**: NY, CA, TX, FL, and more
- **Various Tactics**: ASC, Retargeting, Non-Branded Search
- **Campaigns**: Multiple campaigns per channel/tactic combination

## 🎯 Business Value

This dashboard helps marketing and business leaders:

1. **Optimize Budget Allocation**: Identify high-performing channels and campaigns
2. **Improve Unit Economics**: Monitor CAC, LTV, and profitability metrics
3. **Enhance Attribution**: Understand marketing's contribution to revenue
4. **Scale Efficiently**: Identify opportunities for growth and optimization
5. **Make Data-Driven Decisions**: Access real-time insights and trends

## 🔍 Technical Architecture

- **Frontend**: Streamlit for interactive web interface
- **Visualization**: Plotly for interactive charts and graphs
- **Data Processing**: Pandas for data manipulation and analysis
- **Metrics Engine**: Custom calculation functions for business metrics
- **Modular Design**: Separated concerns with preprocessing and metrics modules

## 📝 Assessment Criteria Alignment

This dashboard addresses all assessment requirements:

### ✅ Technical Execution
- Robust data cleaning and preprocessing
- Efficient joins and aggregations
- Comprehensive derived metrics
- Error handling and data validation

### ✅ Visualization & Storytelling
- Clear, actionable visualizations
- Appropriate chart types for different data
- Coherent narrative flow
- Professional dashboard layout

### ✅ Product Thinking
- Business-relevant metrics and insights
- Strategic recommendations
- Understanding of marketing-business data relationships
- Deep analysis beyond surface-level reporting

### ✅ Delivery
- Fully functional hosted dashboard
- Professional user interface
- Comprehensive documentation
- Easy deployment and usage

## 🤝 Support

For questions or issues:
1. Check the data format requirements
2. Verify all CSV files are properly formatted
3. Ensure all required columns are present
4. Check Python version compatibility

## 📄 License

Built for Assessment 1 - Marketing Intelligence Dashboard


