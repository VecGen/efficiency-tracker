"""
Utility functions for the Developer Efficiency Tracker
"""

from datetime import datetime, timedelta
import hashlib
import urllib.parse
import streamlit as st
from .config import APP_CONFIG


def get_week_dates(date):
    """Get the Monday and Sunday of the week containing the given date"""
    monday = date - timedelta(days=date.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday


def get_current_week():
    """Get the current week's Monday and Sunday"""
    today = datetime.now().date()
    return get_week_dates(today)


def generate_engineer_link(developer_name, team_name, base_url=None):
    """Generate a direct access link for an engineer"""
    if base_url is None:
        base_url = APP_CONFIG['base_url']
    
    # URL encode the parameters
    encoded_dev = urllib.parse.quote(developer_name)
    encoded_team = urllib.parse.quote(team_name)
    
    return f"{base_url}/?dev={encoded_dev}&team={encoded_team}"


def verify_engineer_access(developer_name, team_name, provided_token=None):
    """Verify if the engineer access is valid (simplified for direct access)"""
    # For direct access, we just need valid developer and team names
    # The verification is handled in the main app by checking team configuration
    return True


def get_team_excel_file(team_name):
    """Get the Excel file path for a specific team"""
    return f"efficiency_data_{team_name.replace(' ', '_')}.xlsx"


def format_week_display(monday, sunday):
    """Format week range for display"""
    return f"{monday.strftime('%B %d')} - {sunday.strftime('%B %d, %Y')}"


def apply_custom_css():
    """Apply custom CSS styling to the Streamlit app"""
    css = """
    <style>
    /* Main content styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Header styling */
    .main-header {
        font-size: 2.5rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    
    /* Card styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #2E8B57;
        margin: 1rem 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Form styling */
    .stForm {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
    }
    
    /* Success message styling */
    .stSuccess {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Warning message styling */
    .stWarning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Info message styling */
    .stInfo {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Metric value styling */
    [data-testid="metric-container"] > div > div > div > div {
        color: #2E8B57;
        font-weight: bold;
    }
    
    /* Table styling */
    .stDataFrame {
        background: white;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 8px;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True) 