@echo off
echo Starting Marketing Intelligence Dashboard...
echo.
echo Installing dependencies...
pip install -r src/requirements.txt
echo.
echo Starting Streamlit server...
echo Dashboard will be available at: http://localhost:8501
echo.
streamlit run app.py


