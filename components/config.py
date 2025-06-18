"""
Configuration settings for the Developer Efficiency Tracker
"""
import os

# Application configuration
APP_CONFIG = {
    'title': 'Developer Efficiency Tracker',
    'icon': '🚀',
    'layout': 'wide',
    'base_url': os.environ.get('BASE_URL', 'http://localhost:8501')
}

# AWS S3 Configuration
AWS_CONFIG = {
    'bucket_name': os.environ.get('S3_BUCKET_NAME', 'efficiency-tracker-data'),
    'region': os.environ.get('AWS_REGION', 'us-east-1'),
    'use_s3': os.environ.get('USE_S3', 'false').lower() == 'true'
}

# File paths - local for development, S3 keys for production
FILES = {
    'teams_config': 'teams_config.xlsx',
    'team_settings': 'team_settings.xlsx'
}

# Local data directory for development
LOCAL_DATA_DIR = 'data'

# Default settings
DEFAULT_SETTINGS = {
    'categories': [
        'Feature Development',
        'Bug Fixes',
        'Code Review',
        'Testing',
        'Documentation',
        'Refactoring',
        'API Development',
        'Database Work'
    ],
    'efficiency_areas': [
        'Code Generation',
        'Debugging',
        'Code Completion',
        'Test Writing',
        'Documentation',
        'Refactoring',
        'API Design',
        'Query Optimization'
    ],
    'category_efficiency_mapping': {
        'Feature Development': ['Code Generation', 'API Design', 'Code Completion', 'Documentation'],
        'Bug Fixes': ['Debugging', 'Code Analysis', 'Test Writing', 'Code Completion'],
        'Code Review': ['Code Analysis', 'Code Completion', 'Documentation', 'Refactoring'],
        'Testing': ['Test Writing', 'Code Generation', 'Test Data Creation', 'Debugging'],
        'Documentation': ['Documentation', 'Code Generation', 'API Design', 'Code Completion'],
        'Refactoring': ['Refactoring', 'Code Analysis', 'Code Generation', 'Code Completion'],
        'API Development': ['API Design', 'Code Generation', 'Documentation', 'Test Writing'],
        'Database Work': ['Query Optimization', 'Code Generation', 'Documentation', 'Debugging']
    }
}

# Database columns
DB_COLUMNS = [
    'Week_Start',
    'Week_End', 
    'Story_ID',
    'Developer_Name',
    'Team_Name',
    'Original_Estimate_Hours',
    'Efficiency_Gained_Hours',
    'Copilot_Used',
    'Category',
    'Areas_of_Efficiency',
    'Notes_Observations'
]

# Custom CSS styling
CUSTOM_CSS = """
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1f77b4;
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .warning-message {
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ffeaa7;
        margin: 1rem 0;
    }
    
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    
    .info-box {
        background: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
    
    .team-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        text-align: center;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    .form-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
    }
    
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
    }
    
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .data-table {
        background: white;
        border-radius: 0.5rem;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .sidebar-section {
        margin-bottom: 2rem;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 0.5rem;
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.875rem;
        font-weight: bold;
        text-align: center;
    }
    
    .status-success {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .status-warning {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    
    .status-error {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    
    .feature-highlight {
        background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%);
        border: 1px solid #667eea44;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .progress-bar {
        background: #e9ecef;
        border-radius: 0.25rem;
        height: 1rem;
        overflow: hidden;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 100%;
        transition: width 0.3s ease;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Custom selectbox styling */
    .stSelectbox > div > div > select {
        border-radius: 0.5rem;
        border: 2px solid #e9ecef;
        transition: border-color 0.3s ease;
    }
    
    .stSelectbox > div > div > select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
    }
    
    /* Custom input styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: 0.5rem;
        border: 2px solid #e9ecef;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
    }
    
    /* Alert styling */
    .alert {
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
        border: 1px solid transparent;
    }
    
    .alert-success {
        color: #155724;
        background-color: #d4edda;
        border-color: #c3e6cb;
    }
    
    .alert-warning {
        color: #856404;
        background-color: #fff3cd;
        border-color: #ffeaa7;
    }
    
    .alert-error {
        color: #721c24;
        background-color: #f8d7da;
        border-color: #f5c6cb;
    }
    
    .alert-info {
        color: #0c5460;
        background-color: #d1ecf1;
        border-color: #bee5eb;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .metric-container {
            flex-direction: column;
        }
        
        .chart-container {
            margin: 0.5rem 0;
        }
    }
    
    /* Loading animation */
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
        margin: 2rem auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Card hover effects */
    .hover-card {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .hover-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
    }
    
    /* Enhanced form styling */
    .form-container {
        background: white;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .form-group {
        margin-bottom: 1.5rem;
    }
    
    .form-label {
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    /* Dashboard enhancements */
    .dashboard-card {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    
    .dashboard-metric {
        text-align: center;
        padding: 1rem;
    }
    
    .dashboard-metric h3 {
        color: #667eea;
        margin-bottom: 0.5rem;
        font-size: 2rem;
        font-weight: bold;
    }
    
    .dashboard-metric p {
        color: #666;
        font-size: 0.9rem;
        margin: 0;
    }
    
    /* Enhanced table styling */
    .custom-table {
        border-collapse: collapse;
        width: 100%;
        background: white;
        border-radius: 0.5rem;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .custom-table th {
        background: #667eea;
        color: white;
        padding: 1rem;
        text-align: left;
        font-weight: 600;
    }
    
    .custom-table td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid #e9ecef;
    }
    
    .custom-table tr:hover {
        background-color: #f8f9fa;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        font-size: 0.75rem;
        font-weight: 700;
        line-height: 1;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 0.375rem;
    }
    
    .badge-success {
        color: #fff;
        background-color: #28a745;
    }
    
    .badge-warning {
        color: #212529;
        background-color: #ffc107;
    }
    
    .badge-danger {
        color: #fff;
        background-color: #dc3545;
    }
    
    .badge-info {
        color: #fff;
        background-color: #17a2b8;
    }
    
    .badge-primary {
        color: #fff;
        background-color: #667eea;
    }
</style>
""" 