#!/bin/bash
# deploy.sh - Deployment script for Marketing Intelligence Dashboard

echo "🚀 Deploying Marketing Intelligence Dashboard..."

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
python_version=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Python version: $python_version"

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r src/requirements.txt

# Test imports
echo "🧪 Testing imports..."
python -c "
try:
    import streamlit
    import pandas
    import numpy
    import plotly
    print('✅ All dependencies imported successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')
    exit(1)
"

# Test data loading
echo "📊 Testing data loading..."
python -c "
try:
    from src.preprocess import load_and_merge
    mkt, biz = load_and_merge('data/Facebook.csv', 'data/Google.csv', 'data/TikTok.csv', 'data/Business.csv')
    print(f'✅ Data loaded successfully: {len(mkt)} marketing rows, {len(biz)} business rows')
except Exception as e:
    print(f'❌ Data loading error: {e}')
    exit(1)
"

echo "🎉 Deployment preparation complete!"
echo ""
echo "To run the dashboard:"
echo "  streamlit run app.py"
echo ""
echo "To deploy to Streamlit Cloud:"
echo "  1. Push code to GitHub"
echo "  2. Connect to Streamlit Cloud"
echo "  3. Deploy with automatic updates"
echo ""
echo "To deploy to Heroku:"
echo "  1. Install Heroku CLI"
echo "  2. heroku create your-app-name"
echo "  3. git push heroku main"
