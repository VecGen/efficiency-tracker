"""
Developer Efficiency Tracker - Main Streamlit Application
An application to track and analyze productivity gains from AI coding assistants.
"""

import streamlit as st
import os
import pandas as pd
from datetime import datetime
import hashlib

# Import custom components
from components.s3_data_manager import get_teams_config_manager, get_data_manager
from components.admin_interface import AdminInterface
from components.engineer_interface import EngineerInterface
from components.utils import apply_custom_css

# Page configuration
st.set_page_config(
    page_title="Developer Efficiency Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_admin_password_hash():
    """Get the admin password hash from environment or use default"""
    # In production, set ADMIN_PASSWORD environment variable
    # For development, use default password 'admin123'
    password = os.environ.get("ADMIN_PASSWORD", "admin123")
    return hashlib.sha256(password.encode()).hexdigest()

def verify_admin_password(input_password):
    """Verify admin password"""
    input_hash = hashlib.sha256(input_password.encode()).hexdigest()
    return input_hash == get_admin_password_hash()

def parse_engineer_link():
    """Parse URL parameters to extract engineer and team info"""
    try:
        # Get URL parameters
        params = st.query_params
        
        if "dev" in params and "team" in params:
            developer_name = params["dev"]
            team_name = params["team"]
            
            # Verify this is a valid engineer-team combination
            teams_config_manager = get_teams_config_manager()
            teams_config = teams_config_manager.load_teams_config()
            
            if team_name in teams_config:
                team_config = teams_config[team_name]
                # Handle both old and new data structures
                if isinstance(team_config, dict) and 'developers' in team_config:
                    developers = team_config['developers']
                elif isinstance(team_config, list):
                    developers = [dev['name'] if isinstance(dev, dict) else dev for dev in team_config]
                else:
                    developers = []
                
                if developer_name in developers:
                    return developer_name, team_name
        
        return None, None
    except Exception:
        return None, None

def render_admin_login():
    """Render admin login form"""
    st.markdown("""
    <div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin: 20px 0;">
        <h1 style="color: white; margin-bottom: 20px;">🔧 Admin Access</h1>
        <p style="color: white; opacity: 0.8; font-size: 18px;">Enter admin password to continue</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("admin_login"):
        password = st.text_input("Admin Password", type="password", placeholder="Enter admin password")
        submitted = st.form_submit_button("🔓 Login", type="primary")
        
        if submitted:
            if verify_admin_password(password):
                st.session_state.admin_authenticated = True
                st.success("✅ Admin access granted!")
                st.rerun()
            else:
                st.error("❌ Invalid password. Please try again.")
    
    # Development hint
    if os.environ.get("ADMIN_PASSWORD"):
        st.info("💡 Using custom admin password from environment variable")
    else:
        st.info("💡 Development mode: Default password is 'admin123'")

def main():
    """Main application entry point"""
    
    # Apply custom CSS
    apply_custom_css()
    
    # Initialize data managers
    teams_config_manager = get_teams_config_manager()
    data_manager = get_data_manager()
    
    # Initialize session state
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    
    # Load teams configuration
    teams_config = teams_config_manager.load_teams_config()
    
    # Check for direct engineer access via URL parameters
    engineer_name, team_name = parse_engineer_link()
    
    if engineer_name and team_name:
        # Direct engineer access
        st.sidebar.markdown("""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 20px;">
            <h3 style="color: white; margin: 0;">👋 Welcome!</h3>
            <p style="color: white; opacity: 0.9; margin: 10px 0 0 0;">{}</p>
            <p style="color: white; opacity: 0.7; margin: 5px 0 0 0;">Team: {}</p>
        </div>
        """.format(engineer_name, team_name), unsafe_allow_html=True)
        
        # Quick stats in sidebar
        st.sidebar.markdown("### 📈 Quick Stats")
        
        try:
            from components.utils import get_team_excel_file
            team_file = get_team_excel_file(team_name)
            df = data_manager.load_excel_data(team_file)
            
            if not df.empty:
                user_data = df[df['Developer_Name'] == engineer_name]
                if not user_data.empty:
                    total_saved = user_data['Efficiency_Gained_Hours'].sum()
                    entries_count = len(user_data)
                    
                    st.sidebar.metric("Your Total Time Saved", f"{total_saved:.1f}h")
                    st.sidebar.metric("Your Total Entries", entries_count)
                else:
                    st.sidebar.info("No entries yet. Start logging your efficiency gains!")
            else:
                st.sidebar.info("No data available yet.")
                
        except Exception as e:
            st.sidebar.error(f"Error loading stats: {str(e)}")
        
        # Admin access link
        st.sidebar.markdown("---")
        if st.sidebar.button("🔧 Admin Access"):
            # Clear URL parameters and redirect to admin
            st.query_params.clear()
            st.rerun()
        
        # Render engineer interface
        engineer_interface = EngineerInterface(engineer_name, team_name)
        engineer_interface.render()
        
    elif st.query_params.get("admin") == "true" or st.session_state.admin_authenticated:
        # Admin access
        if not st.session_state.admin_authenticated:
            render_admin_login()
        else:
            # Show admin sidebar info
            st.sidebar.markdown("""
            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 20px;">
                <h3 style="color: white; margin: 0;">🔧 Admin Panel</h3>
                <p style="color: white; opacity: 0.9; margin: 10px 0 0 0;">System Administration</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Admin actions
            st.sidebar.markdown("### 🎛️ Admin Actions")
            if st.sidebar.button("🔓 Logout"):
                st.session_state.admin_authenticated = False
                st.query_params.clear()
                st.rerun()
            
            # If no teams configured, show setup message
            if not teams_config:
                st.warning("⚠️ No teams configured. Please set up your first team below.")
            
            # Render admin interface
            admin_interface = AdminInterface()
            admin_interface.render()
    
    else:
        # Landing page - show options to access admin or engineer selection
        st.markdown("""
        <div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin: 20px 0;">
            <h1 style="color: white; margin-bottom: 20px;">📊 Developer Efficiency Tracker</h1>
            <h3 style="color: white; opacity: 0.9; margin-bottom: 30px;">Track and analyze productivity gains from AI coding assistants</h3>
            <p style="color: white; opacity: 0.8; font-size: 18px;">Choose your access method below</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Access options
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("### 🚪 Access Options")
            
            # Admin access button
            if st.button("🔧 Admin Access", use_container_width=True, type="primary"):
                st.query_params["admin"] = "true"
                st.rerun()
            
            st.markdown("---")
            
            # Engineer selection (fallback for those without direct links)
            if teams_config:
                st.markdown("### 👩‍💻 Engineer Access")
                st.info("💡 **Engineers:** Use your personal access link for direct access, or select your team below:")
                
                team_names = list(teams_config.keys())
                selected_team = st.selectbox(
                    "Select Your Team",
                    ["Select a team"] + team_names,
                    key="team_selector"
                )
                
                if selected_team != "Select a team":
                    team_config = teams_config[selected_team]
                    # Handle both old and new data structures
                    if isinstance(team_config, dict) and 'developers' in team_config:
                        developers = team_config['developers']
                    elif isinstance(team_config, list):
                        developers = [dev['name'] if isinstance(dev, dict) else dev for dev in team_config]
                    else:
                        developers = []
                    
                    if developers:
                        selected_developer = st.selectbox(
                            "Select Your Name",
                            ["Select your name"] + developers,
                            key="dev_selector"
                        )
                        
                        if selected_developer != "Select your name":
                            # Redirect to engineer interface with URL parameters
                            st.query_params["dev"] = selected_developer
                            st.query_params["team"] = selected_team
                            st.rerun()
                    else:
                        st.warning("No developers configured for this team. Please contact your admin.")
            else:
                st.info("👩‍💻 **Engineers:** No teams configured yet. Please contact your admin to set up access.")
        
        # Feature overview
        st.markdown("### ✨ Features")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: #f8f9fa; padding: 30px; border-radius: 10px; text-align: center; height: 300px;">
                <h3>👩‍💻 For Engineers</h3>
                <ul style="text-align: left; margin-top: 20px;">
                    <li>Direct access via personal links</li>
                    <li>Log weekly efficiency gains</li>
                    <li>Track time saved with AI tools</li>
                    <li>View personal analytics</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: #f8f9fa; padding: 30px; border-radius: 10px; text-align: center; height: 300px;">
                <h3>🔧 For Admins</h3>
                <ul style="text-align: left; margin-top: 20px;">
                    <li>Password-protected access</li>
                    <li>Manage teams and developers</li>
                    <li>Generate team reports</li>
                    <li>Export data for analysis</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: #f8f9fa; padding: 30px; border-radius: 10px; text-align: center; height: 300px;">
                <h3>📈 Analytics</h3>
                <ul style="text-align: left; margin-top: 20px;">
                    <li>Real-time efficiency metrics</li>
                    <li>Trend analysis</li>
                    <li>Category breakdowns</li>
                    <li>Team comparisons</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    # Get port from environment variable (for App Runner)
    port = int(os.environ.get("PORT", 8501))
    
    # For local development, run normally
    # For cloud deployment, the web server handles this
    main() 