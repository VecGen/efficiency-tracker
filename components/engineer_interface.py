"""
Engineer interface components for the Developer Efficiency Tracker
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from .s3_data_manager import get_data_manager, get_team_settings_manager
from .utils import get_week_dates, get_current_week, get_team_excel_file, format_week_display


class EngineerInterface:
    """Handles the engineer-specific interface"""
    
    def __init__(self, developer_name, team_name):
        self.developer_name = developer_name
        self.team_name = team_name
        self.team_file = get_team_excel_file(team_name)
        self.data_manager = get_data_manager()
        self.settings_manager = get_team_settings_manager()
    
    def render(self):
        """Render the complete engineer interface"""
        st.markdown(f'<h1 class="main-header">👋 Welcome, {self.developer_name}!</h1>', 
                   unsafe_allow_html=True)
        st.markdown(f"**Team:** {self.team_name}")
        
        # Load engineer's data
        df = self.data_manager.load_excel_data(self.team_file)
        engineer_df = df[df['Developer_Name'] == self.developer_name] if not df.empty else pd.DataFrame()
        
        # Navigation tabs
        tab1, tab2 = st.tabs(["📝 Add Entry", "📊 My Data"])
        
        with tab1:
            self._render_data_entry()
        
        with tab2:
            self._render_dashboard(engineer_df)
    
    def _render_data_entry(self):
        """Render the simplified data entry form"""
        st.header("📝 Log your weekly update")
        
        # Load existing data and settings
        df = self.data_manager.load_excel_data(self.team_file)
        settings = self.settings_manager.load_team_settings()
        
        # Get current week info
        current_monday, current_sunday = get_current_week()
        
        # Initialize session state for form clearing
        if 'form_submitted' not in st.session_state:
            st.session_state.form_submitted = False
        if 'clear_form' not in st.session_state:
            st.session_state.clear_form = False
        if 'form_version' not in st.session_state:
            st.session_state.form_version = 0
        
        # Week selection OUTSIDE the form for real-time updates
        week_date = st.date_input(
            "Select Week", 
            value=current_monday,
            max_value=current_sunday,  # Prevent future weeks
            help="Select any date within the week you want to log. You cannot select future weeks."
        )
        
        # Calculate and display the week range - updates in real-time
        selected_monday, selected_sunday = get_week_dates(week_date)
        st.info(f"📅 **Selected Week:** {format_week_display(selected_monday, selected_sunday)}")
        
        # Copilot usage selection OUTSIDE the form for real-time conditional display
        copilot_used = st.selectbox(
            "Used Copilot?", 
            ["Yes", "No"],
            index=0,
            key=f"copilot_used_input_{st.session_state.form_version}",
            help="Select whether you used GitHub Copilot for this task"
        )
        
        # Category to efficiency areas mapping
        # Use team settings mapping if available, otherwise use default mapping
        team_mapping = settings.get('category_efficiency_mapping', {})
        default_mapping = {
            'Feature Development': ['Code Generation', 'API Design', 'Code Completion', 'Documentation'],
            'Bug Fixes': ['Debugging', 'Code Analysis', 'Test Writing', 'Code Completion'],
            'Code Review': ['Code Analysis', 'Code Completion', 'Documentation', 'Refactoring'],
            'Testing': ['Test Writing', 'Code Generation', 'Test Data Creation', 'Debugging'],
            'Documentation': ['Documentation', 'Code Generation', 'API Design', 'Code Completion'],
            'Refactoring': ['Refactoring', 'Code Analysis', 'Code Generation', 'Code Completion'],
            'API Development': ['API Design', 'Code Generation', 'Documentation', 'Test Writing'],
            'Database Work': ['Query Optimization', 'Code Generation', 'Documentation', 'Debugging']
        }
        
        # Task Category selection OUTSIDE the form for real-time efficiency areas updates
        category = st.selectbox(
            "Task Category",
            settings['categories'],
            index=0,
            help="Select the type of task you worked on:",
            key=f"category_selector_{st.session_state.form_version}"
        )
        
        # Conditional efficiency areas section - OUTSIDE the form for real-time updates
        selected_areas = []
        if copilot_used == "Yes":
            st.subheader("🎯 Where did Copilot help?")
            
            # Dynamic efficiency areas based on selected category
            # First check team settings mapping, then default mapping, finally all areas
            if category in team_mapping and team_mapping[category]:
                available_areas = team_mapping[category]
                st.caption(f"💡 Showing configured areas for **{category}**")
            elif category in default_mapping:
                available_areas = default_mapping[category]
                st.caption(f"💡 Showing default areas most relevant to **{category}**")
            else:
                available_areas = settings['efficiency_areas']
                st.caption("💡 Showing all available efficiency areas")
            
            # Efficiency areas selection
            area_cols = st.columns(2)  # Two columns for better layout
            
            for i, area in enumerate(available_areas):
                col_idx = i % 2
                with area_cols[col_idx]:
                    checkbox_key = f"area_{area}_{category}_{st.session_state.form_version}"
                    if st.checkbox(
                        area, 
                        key=checkbox_key,
                        value=False
                    ):
                        selected_areas.append(area)
            
            # Show selected areas summary
            if selected_areas:
                st.info(f"🎯 **Selected Efficiency Areas:** {', '.join(selected_areas)}")
            else:
                st.warning("⚠️ Please select at least one efficiency area above")
        
        # Form for the remaining basic fields
        with st.form("engineer_entry_form", clear_on_submit=True):
            st.subheader("📝 Task Details")
            
            col1, col2 = st.columns(2)
            
            with col1:
                story_id = st.text_input(
                    "Story/Task ID", 
                    placeholder="e.g., ENG-1542",
                    key=f"story_id_input_{st.session_state.form_version}"
                )
            
            with col2:
                original_estimate = st.number_input(
                    "Original Estimate (Hours)", 
                    min_value=0.0, 
                    step=0.5, 
                    value=0.0,
                    help="How long would this have taken without Copilot?",
                    key=f"original_estimate_input_{st.session_state.form_version}"
                )
            
            # Show time saved input only when Copilot was used
            if copilot_used == "Yes":
                efficiency_gained = st.number_input(
                    "Time Saved (Hours)", 
                    min_value=0.0, 
                    step=0.5, 
                    value=0.0,
                    help="How much time did Copilot save you?",
                    key=f"efficiency_gained_input_{st.session_state.form_version}"
                )
            else:
                # When Copilot wasn't used, set efficiency gained to 0 and show info
                efficiency_gained = 0.0
                st.info("💡 Time saved set to 0 since Copilot wasn't used")
            
            notes = st.text_area(
                "Notes (Optional)", 
                placeholder="e.g., Copilot generated the entire API endpoint, Helped debug complex logic",
                key=f"notes_input_{st.session_state.form_version}"
            )
            
            # Form submission
            col_submit_1, col_submit_2 = st.columns([1, 3])
            with col_submit_1:
                submitted = st.form_submit_button("💾 Save Entry", type="primary")
            with col_submit_2:
                if st.form_submit_button("🔄 Clear Form", type="secondary"):
                    # Increment form version to reset all widgets
                    st.session_state.form_version += 1
                    st.rerun()
            
            if submitted:
                # Validation logic updated for conditional Copilot usage
                validation_passed = True
                error_messages = []
                
                if not story_id:
                    error_messages.append("Story ID is required")
                    validation_passed = False
                
                if original_estimate <= 0:
                    error_messages.append("Original Estimate must be greater than 0")
                    validation_passed = False
                
                if copilot_used == "Yes" and not selected_areas:
                    error_messages.append("Please select at least one efficiency area when Copilot was used")
                    validation_passed = False
                
                if validation_passed:
                    success = self._save_entry(df, selected_monday, selected_sunday, story_id, 
                                             original_estimate, efficiency_gained, copilot_used, 
                                             category, selected_areas, notes)
                    if success:
                        # Show success message with details
                        st.success("✅ Entry saved successfully!")
                        st.balloons()
                        
                        # Show summary of what was saved
                        with st.expander("📋 Entry Summary", expanded=True):
                            col_sum1, col_sum2 = st.columns(2)
                            with col_sum1:
                                st.write(f"**Story ID:** {story_id}")
                                st.write(f"**Category:** {category}")
                                st.write(f"**Original Estimate:** {original_estimate} hours")
                                if copilot_used == "Yes":
                                    st.write(f"**Time Saved:** {efficiency_gained} hours")
                            with col_sum2:
                                st.write(f"**Copilot Used:** {copilot_used}")
                                st.write(f"**Week:** {format_week_display(selected_monday, selected_sunday)}")
                                if copilot_used == "Yes" and selected_areas:
                                    st.write(f"**Efficiency Areas:** {', '.join(selected_areas)}")
                                if notes:
                                    st.write(f"**Notes:** {notes}")
                        
                        # Increment form version to clear all fields for next entry
                        st.session_state.form_version += 1
                        st.info("🔄 Form cleared automatically for your next entry...")
                        st.rerun()
                else:
                    for error in error_messages:
                        st.error(f"❌ {error}")
    
    def _save_entry(self, df, selected_monday, selected_sunday, story_id, 
                   original_estimate, efficiency_gained, copilot_used, 
                   category, selected_areas, notes):
        """Save a new entry to the database"""
        try:
            new_row = {
                'Week_Start': selected_monday.strftime('%Y-%m-%d'),
                'Week_End': selected_sunday.strftime('%Y-%m-%d'),
                'Story_ID': story_id,
                'Developer_Name': self.developer_name,
                'Team_Name': self.team_name,
                'Original_Estimate_Hours': original_estimate,
                'Efficiency_Gained_Hours': efficiency_gained,
                'Copilot_Used': copilot_used,
                'Category': category,
                'Areas_of_Efficiency': ', '.join(selected_areas) if selected_areas else '',
                'Notes_Observations': notes
            }
            
            # Add to DataFrame
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            
            # Save to Excel
            if self.data_manager.save_to_excel(df, self.team_file):
                return True
            else:
                st.error("❌ Failed to save entry to database!")
                return False
                
        except Exception as e:
            st.error(f"❌ Error saving entry: {str(e)}")
            return False
    
    def _render_dashboard(self, engineer_df):
        """Render the personal dashboard for engineers"""
        st.header("📊 Your Efficiency Summary")
        
        if engineer_df.empty:
            st.info("No entries yet. Start logging your efficiency gains!")
            return
        
        # Personal metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_time_saved = engineer_df['Efficiency_Gained_Hours'].sum()
            st.metric("Total Time Saved", f"{total_time_saved:.1f} hours")
        
        with col2:
            avg_efficiency = (engineer_df['Efficiency_Gained_Hours'] / 
                            engineer_df['Original_Estimate_Hours'] * 100).mean()
            st.metric("Average Efficiency", f"{avg_efficiency:.1f}%")
        
        with col3:
            total_entries = len(engineer_df)
            st.metric("Total Entries", total_entries)
        
        # Personal visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            self._render_category_chart(engineer_df)
        
        with col2:
            self._render_trend_chart(engineer_df)
        
        # Recent entries
        self._render_recent_entries(engineer_df)
    
    def _render_category_chart(self, engineer_df):
        """Render efficiency by category chart"""
        cat_data = engineer_df.groupby('Category')['Efficiency_Gained_Hours'].sum().reset_index()
        if not cat_data.empty:
            fig = px.bar(cat_data, x='Category', y='Efficiency_Gained_Hours',
                        title='Your Time Saved by Category')
            st.plotly_chart(fig, use_container_width=True)
    
    def _render_trend_chart(self, engineer_df):
        """Render weekly efficiency trend chart"""
        # Handle both old and new date formats
        if 'Week_Start' in engineer_df.columns:
            engineer_df['Week'] = pd.to_datetime(engineer_df['Week_Start'])
        else:
            engineer_df['Week'] = pd.to_datetime(engineer_df['Week'])
        
        weekly_data = engineer_df.groupby('Week')['Efficiency_Gained_Hours'].sum().reset_index()
        if not weekly_data.empty:
            fig = px.line(weekly_data, x='Week', y='Efficiency_Gained_Hours',
                         title='Your Weekly Efficiency Trend')
            st.plotly_chart(fig, use_container_width=True)
    
    def _render_recent_entries(self, engineer_df):
        """Render recent entries table"""
        st.subheader("📋 Your Recent Entries")
        display_columns = ['Story_ID', 'Category', 'Original_Estimate_Hours', 
                          'Efficiency_Gained_Hours', 'Copilot_Used']
        
        # Handle both old and new date formats for display
        if 'Week_Start' in engineer_df.columns:
            recent_entries = engineer_df.sort_values('Week_Start', ascending=False).head(10)
            display_columns = ['Week_Start', 'Week_End'] + display_columns
        else:
            recent_entries = engineer_df.sort_values('Week', ascending=False).head(10)
            display_columns = ['Week'] + display_columns
        
        # Only show columns that exist
        available_columns = [col for col in display_columns if col in recent_entries.columns]
        st.dataframe(recent_entries[available_columns], use_container_width=True) 