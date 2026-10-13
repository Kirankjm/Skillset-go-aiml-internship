@echo off
echo Starting Perfect Fitness Agent Web Interface...
echo.
echo The web interface will open in your browser automatically.
echo If it doesn't open, go to: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server.
echo.
streamlit run web_interface.py --server.headless true
