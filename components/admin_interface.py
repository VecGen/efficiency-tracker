"""
Admin interface components for the Developer Efficiency Tracker
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from io import BytesIO
from .s3_data_manager import get_data_manager, get_teams_config_manager, get_team_settings_manager
from .utils import generate_engineer_link, get_team_excel_file


class AdminInterface:
    """Handles the admin-specific interface"""
    
    def __init__(self):
        self.teams_config_manager = get_teams_config_manager()
        self.teams_config = self.teams_config_manager.load_teams_config()
    
    def render(self):
        """Render the complete admin interface"""
        st.markdown('<h1 class="main-header">🛠️ Developer Efficiency Tracker - Admin Panel</h1>', 
                   unsafe_allow_html=True)
        
        # Sidebar navigation
        st.sidebar.title("Admin Navigation")
        page = st.sidebar.selectbox("Choose a page", 
                                  ["Team Setup", "Team Settings", "Dashboard", "Data Management"])
        
        if page == "Team Setup":
            TeamSetupPage(self.teams_config).render()
        elif page == "Team Settings":
            TeamSettingsPage().render()
        elif page == "Dashboard":
            AdminDashboardPage(self.teams_config).render()
        elif page == "Data Management":
            DataManagementPage(self.teams_config).render()


class TeamSetupPage:
    """Handles team setup and configuration"""
    
    def __init__(self, teams_config):
        self.teams_config = teams_config
        self.teams_config_manager = get_teams_config_manager()
    
    def render(self):
        """Render the team setup page"""
        st.header("👥 Team Setup & Management")
        
        # Team management tabs
        tab1, tab2 = st.tabs(["🏢 Manage Teams", "📊 Overview"])
        
        with tab1:
            self._render_team_management()
        
        with tab2:
            self._render_teams_overview()
    
    def _render_team_management(self):
        """Render team management interface"""
        st.subheader("Add New Team")
        
        with st.form("add_team_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                team_name = st.text_input("Team Name", placeholder="e.g., Platform Team")
            
            with col2:
                team_description = st.text_input("Description (Optional)", 
                                               placeholder="Brief team description")
            
            if st.form_submit_button("➕ Create Team", type="primary"):
                if team_name:
                    if team_name not in self.teams_config:
                        self.teams_config[team_name] = []
                        if self.teams_config_manager.save_teams_config(self.teams_config):
                            st.success(f"✅ Team '{team_name}' created successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to save team configuration!")
                    else:
                        st.error(f"❌ Team '{team_name}' already exists!")
                else:
                    st.error("❌ Team name is required!")
        
        if self.teams_config:
            st.subheader("Existing Teams")
            for team_name in self.teams_config.keys():
                self._render_team_editor(team_name)
    
    def _render_team_editor(self, team_name):
        """Render team editor for a specific team"""
        with st.expander(f"🏢 {team_name} ({len(self.teams_config[team_name])} members)"):
            st.markdown(f"**Team:** {team_name}")
            
            # Add developer form
            st.subheader("Add Developer")
            with st.form(f"add_dev_form_{team_name}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    dev_name = st.text_input("Developer Name", 
                                           placeholder="e.g., John Doe",
                                           key=f"dev_name_{team_name}")
                
                with col2:
                    dev_email = st.text_input("Email", 
                                            placeholder="john.doe@company.com",
                                            key=f"dev_email_{team_name}")
                
                if st.form_submit_button("➕ Add Developer"):
                    if dev_name:
                        # Generate access link
                        access_link = generate_engineer_link(dev_name, team_name)
                        
                        developer = {
                            'name': dev_name,
                            'email': dev_email,
                            'link': access_link
                        }
                        
                        self.teams_config[team_name].append(developer)
                        
                        if self.teams_config_manager.save_teams_config(self.teams_config):
                            st.success(f"✅ {dev_name} added to {team_name}!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to save configuration!")
                    else:
                        st.error("❌ Developer name is required!")
            
            # Display existing developers
            if self.teams_config[team_name]:
                st.subheader("Team Members")
                for i, dev in enumerate(self.teams_config[team_name]):
                    with st.container():
                        col1, col2, col3 = st.columns([3, 3, 1])
                        
                        with col1:
                            st.write(f"**{dev['name']}**")
                            if dev.get('email'):
                                st.caption(f"📧 {dev['email']}")
                        
                        with col2:
                            if dev.get('link'):
                                st.code(dev['link'], language=None)
                        
                        with col3:
                            if st.button("🗑️", key=f"delete_{team_name}_{i}", 
                                       help=f"Remove {dev['name']} from team"):
                                self.teams_config[team_name].pop(i)
                                if self.teams_config_manager.save_teams_config(self.teams_config):
                                    st.success(f"✅ {dev['name']} removed from team!")
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to save changes!")
                        
                        st.divider()
            else:
                st.info("No developers added yet. Use the form above to add team members.")
            
            # Team actions
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"📧 Email All Links - {team_name}", key=f"email_team_{team_name}"):
                    self._show_email_template(team_name)
            
            with col2:
                if st.button(f"🗑️ Delete Team - {team_name}", key=f"delete_team_{team_name}",
                           type="secondary"):
                    if st.session_state.get(f"confirm_delete_{team_name}", False):
                        del self.teams_config[team_name]
                        if self.teams_config_manager.save_teams_config(self.teams_config):
                            st.success(f"✅ Team '{team_name}' deleted!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete team!")
                    else:
                        st.session_state[f"confirm_delete_{team_name}"] = True
                        st.warning("⚠️ Click again to confirm deletion!")
    
    def _show_email_template(self, team_name):
        """Show email template for team access links"""
        st.subheader(f"📧 Email Template for {team_name}")
        
        team_members = self.teams_config[team_name]
        if not team_members:
            st.warning("No team members to email!")
            return
        
        email_template = f"""
Subject: Developer Efficiency Tracker - Your Access Link

Hi {{developer_name}},

You now have access to the Developer Efficiency Tracker for {team_name}.

Your personal access link:
{{access_link}}

Please bookmark this link for easy access. You can use it to:
- Log your weekly efficiency data
- Track your personal productivity metrics
- View your efficiency trends over time

If you have any questions, please reach out to your manager.

Best regards,
The Engineering Team
        """
        
        st.text_area("Email Template", value=email_template.strip(), height=300)
        
        st.subheader("Individual Links")
        for dev in team_members:
            st.write(f"**{dev['name']}**")
            if dev.get('email'):
                st.write(f"📧 {dev['email']}")
            if dev.get('link'):
                st.code(dev['link'])
            st.divider()
    
    def _render_teams_overview(self):
        """Render teams overview with statistics"""
        st.subheader("📊 Teams Overview")
        
        if not self.teams_config:
            st.info("No teams configured yet. Create your first team in the 'Manage Teams' tab.")
            return
        
        # Overview metrics
        total_teams = len(self.teams_config)
        total_developers = sum(len(devs) for devs in self.teams_config.values())
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Teams", total_teams)
        with col2:
            st.metric("Total Developers", total_developers)
        
        # Teams breakdown
        st.subheader("Team Breakdown")
        team_data = []
        for team_name, developers in self.teams_config.items():
            team_data.append({
                'Team': team_name,
                'Members': len(developers),
                'Configured Links': sum(1 for dev in developers if dev.get('link'))
            })
        
        if team_data:
            df = pd.DataFrame(team_data)
            st.dataframe(df, use_container_width=True)


class TeamSettingsPage:
    """Handles team settings configuration"""
    
    def __init__(self):
        self.settings_manager = get_team_settings_manager()
    
    def render(self):
        """Render the team settings page"""
        st.header("⚙️ Team Settings Configuration")
        
        # Load current settings
        settings = self.settings_manager.load_team_settings()
        
        # Settings tabs
        tab1, tab2, tab3 = st.tabs(["📋 Categories", "🎯 Efficiency Areas", "🔗 Mappings"])
        
        with tab1:
            self._render_categories_settings(settings)
        
        with tab2:
            self._render_efficiency_areas_settings(settings)
        
        with tab3:
            self._render_mappings_settings(settings)
    
    def _render_categories_settings(self, settings):
        """Render categories configuration"""
        st.subheader("📋 Task Categories")
        st.info("Configure the types of tasks your team works on. These will appear in the data entry form.")
        
        # Current categories
        categories = settings.get('categories', [])
        
        # Add new category
        with st.form("add_category_form"):
            new_category = st.text_input("Add New Category", placeholder="e.g., Performance Optimization")
            if st.form_submit_button("➕ Add Category"):
                if new_category and new_category not in categories:
                    categories.append(new_category)
                    settings['categories'] = categories
                    if self.settings_manager.save_team_settings(settings):
                        st.success(f"✅ Added category: {new_category}")
                        st.rerun()
                    else:
                        st.error("❌ Failed to save settings!")
                elif new_category in categories:
                    st.error("❌ Category already exists!")
        
        # Display and manage existing categories
        if categories:
            st.subheader("Current Categories")
            for i, category in enumerate(categories):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"• {category}")
                with col2:
                    if st.button("🗑️", key=f"delete_cat_{i}", help=f"Delete {category}"):
                        categories.pop(i)
                        settings['categories'] = categories
                        if self.settings_manager.save_team_settings(settings):
                            st.success(f"✅ Deleted category: {category}")
                            st.rerun()
                        else:
                            st.error("❌ Failed to save settings!")
        else:
            st.info("No categories configured yet.")
    
    def _render_efficiency_areas_settings(self, settings):
        """Render efficiency areas configuration"""
        st.subheader("🎯 Efficiency Areas")
        st.info("Configure the areas where Copilot can help. These will appear when logging efficiency data.")
        
        # Current efficiency areas
        efficiency_areas = settings.get('efficiency_areas', [])
        
        # Add new area
        with st.form("add_area_form"):
            new_area = st.text_input("Add New Efficiency Area", placeholder="e.g., Unit Test Generation")
            if st.form_submit_button("➕ Add Area"):
                if new_area and new_area not in efficiency_areas:
                    efficiency_areas.append(new_area)
                    settings['efficiency_areas'] = efficiency_areas
                    if self.settings_manager.save_team_settings(settings):
                        st.success(f"✅ Added efficiency area: {new_area}")
                        st.rerun()
                    else:
                        st.error("❌ Failed to save settings!")
                elif new_area in efficiency_areas:
                    st.error("❌ Efficiency area already exists!")
        
        # Display and manage existing areas
        if efficiency_areas:
            st.subheader("Current Efficiency Areas")
            for i, area in enumerate(efficiency_areas):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"• {area}")
                with col2:
                    if st.button("🗑️", key=f"delete_area_{i}", help=f"Delete {area}"):
                        efficiency_areas.pop(i)
                        settings['efficiency_areas'] = efficiency_areas
                        if self.settings_manager.save_team_settings(settings):
                            st.success(f"✅ Deleted efficiency area: {area}")
                            st.rerun()
                        else:
                            st.error("❌ Failed to save settings!")
        else:
            st.info("No efficiency areas configured yet.")
    
    def _render_mappings_settings(self, settings):
        """Render category to efficiency areas mappings"""
        st.subheader("🔗 Category → Efficiency Areas Mapping")
        st.info("Map task categories to relevant efficiency areas. This helps engineers see the most relevant options.")
        
        categories = settings.get('categories', [])
        efficiency_areas = settings.get('efficiency_areas', [])
        mappings = settings.get('category_efficiency_mapping', {})
        
        if not categories or not efficiency_areas:
            st.warning("⚠️ Please configure categories and efficiency areas first before setting up mappings.")
            return
        
        # Configure mappings
        for category in categories:
            with st.expander(f"🏷️ {category}"):
                current_mapping = mappings.get(category, [])
                
                # Multi-select for efficiency areas
                selected_areas = st.multiselect(
                    f"Select efficiency areas for {category}",
                    efficiency_areas,
                    default=current_mapping,
                    key=f"mapping_{category}"
                )
                
                if st.button(f"💾 Save Mapping for {category}", key=f"save_mapping_{category}"):
                    mappings[category] = selected_areas
                    settings['category_efficiency_mapping'] = mappings
                    if self.settings_manager.save_team_settings(settings):
                        st.success(f"✅ Saved mapping for {category}")
                        st.rerun()
                    else:
                        st.error("❌ Failed to save mapping!")
                
                if current_mapping:
                    st.write("**Current mapping:**")
                    for area in current_mapping:
                        st.write(f"• {area}")
                else:
                    st.info("No areas mapped yet - will show all areas to engineers")


class AdminDashboardPage:
    """Handles admin dashboard with cross-team analytics"""
    
    def __init__(self, teams_config):
        self.teams_config = teams_config
        self.data_manager = get_data_manager()
    
    def render(self):
        """Render the admin dashboard"""
        st.header("📊 Admin Dashboard - All Teams Overview")
        
        if not self.teams_config:
            st.warning("No teams configured yet. Please set up teams first.")
            return
        
        # Aggregate data from all teams
        all_data, team_stats = self._aggregate_team_data()
        
        if not all_data:
            st.warning("No data available yet. Engineers need to start logging their efficiency data.")
            return
        
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Render dashboard sections
        self._render_key_metrics(combined_df)
        self._render_team_comparison(team_stats)
        self._render_visualizations(combined_df)
    
    def _aggregate_team_data(self):
        """Aggregate data from all teams"""
        all_data = []
        team_stats = {}
        
        for team_name in self.teams_config.keys():
            team_file = get_team_excel_file(team_name)
            team_df = self.data_manager.load_excel_data(team_file)
            
            if not team_df.empty:
                all_data.append(team_df)
                team_stats[team_name] = {
                    'entries': len(team_df),
                    'total_time_saved': team_df['Efficiency_Gained_Hours'].sum(),
                    'avg_efficiency': (team_df['Efficiency_Gained_Hours'] / 
                                     team_df['Original_Estimate_Hours'] * 100).mean(),
                    'copilot_usage': (team_df['Copilot_Used'] == 'Yes').mean() * 100
                }
        
        return all_data, team_stats
    
    def _render_key_metrics(self, combined_df):
        """Render key performance metrics"""
        st.subheader("🎯 Key Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_time_saved = combined_df['Efficiency_Gained_Hours'].sum()
            st.metric("Total Time Saved", f"{total_time_saved:.1f} hours")
        
        with col2:
            avg_efficiency = (combined_df['Efficiency_Gained_Hours'] / 
                            combined_df['Original_Estimate_Hours'] * 100).mean()
            st.metric("Average Efficiency", f"{avg_efficiency:.1f}%")
        
        with col3:
            copilot_usage = (combined_df['Copilot_Used'] == 'Yes').mean() * 100
            st.metric("Copilot Usage Rate", f"{copilot_usage:.1f}%")
        
        with col4:
            total_entries = len(combined_df)
            st.metric("Total Entries", total_entries)
    
    def _render_team_comparison(self, team_stats):
        """Render team comparison table"""
        st.subheader("🏢 Team Performance Comparison")
        
        if team_stats:
            comparison_data = []
            for team_name, stats in team_stats.items():
                comparison_data.append({
                    'Team': team_name,
                    'Entries': stats['entries'],
                    'Total Time Saved (h)': f"{stats['total_time_saved']:.1f}",
                    'Avg Efficiency (%)': f"{stats['avg_efficiency']:.1f}",
                    'Copilot Usage (%)': f"{stats['copilot_usage']:.1f}"
                })
            
            df = pd.DataFrame(comparison_data)
            st.dataframe(df, use_container_width=True)
    
    def _render_visualizations(self, combined_df):
        """Render dashboard visualizations"""
        col1, col2 = st.columns(2)
        
        with col1:
            # Team efficiency comparison
            team_efficiency = combined_df.groupby('Team_Name')['Efficiency_Gained_Hours'].sum().reset_index()
            if not team_efficiency.empty:
                fig = px.bar(team_efficiency, x='Team_Name', y='Efficiency_Gained_Hours',
                           title='Total Time Saved by Team')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Category breakdown
            category_data = combined_df.groupby('Category')['Efficiency_Gained_Hours'].sum().reset_index()
            if not category_data.empty:
                fig = px.pie(category_data, values='Efficiency_Gained_Hours', names='Category',
                           title='Time Saved by Category')
                st.plotly_chart(fig, use_container_width=True)


class DataManagementPage:
    """Handles data export and management"""
    
    def __init__(self, teams_config):
        self.teams_config = teams_config
        self.data_manager = get_data_manager()
    
    def render(self):
        """Render the data management page"""
        st.header("🗂️ Data Management")
        
        if not self.teams_config:
            st.warning("No teams configured yet.")
            return
        
        # Export section
        self._render_export_section()
        
        # Individual team data section
        self._render_individual_team_data()
    
    def _render_export_section(self):
        """Render data export section"""
        st.subheader("📤 Export Team Data")
        selected_teams = st.multiselect("Select teams to export", list(self.teams_config.keys()))
        
        if selected_teams:
            # Prepare combined data
            combined_data = []
            for team_name in selected_teams:
                team_file = get_team_excel_file(team_name)
                team_df = self.data_manager.load_excel_data(team_file)
                if not team_df.empty:
                    combined_data.append(team_df)
            
            if combined_data:
                combined_df = pd.concat(combined_data, ignore_index=True)
                excel_buffer = BytesIO()
                combined_df.to_excel(excel_buffer, index=False)
                excel_buffer.seek(0)
                
                st.write(f"**Ready to download:** {len(combined_df)} entries from {len(selected_teams)} team(s)")
                
                st.download_button(
                    label="📥 Download Combined Excel",
                    data=excel_buffer.getvalue(),
                    file_name=f"efficiency_data_combined_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_combined",
                    use_container_width=True
                )
            else:
                st.warning("No data available for selected teams.")
    
    def _create_combined_export(self, selected_teams):
        """Create and offer combined Excel download"""
        combined_data = []
        for team_name in selected_teams:
            team_file = get_team_excel_file(team_name)
            team_df = self.data_manager.load_excel_data(team_file)
            if not team_df.empty:
                combined_data.append(team_df)
        
        if combined_data:
            combined_df = pd.concat(combined_data, ignore_index=True)
            excel_buffer = BytesIO()
            combined_df.to_excel(excel_buffer, index=False)
            excel_buffer.seek(0)
            
            st.download_button(
                label="Download Excel File",
                data=excel_buffer,
                file_name=f"efficiency_data_combined_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    def _render_individual_team_data(self):
        """Render individual team data management"""
        st.subheader("📋 Individual Team Data")
        for team_name in self.teams_config.keys():
            with st.expander(f"📊 {team_name} Data"):
                team_file = get_team_excel_file(team_name)
                team_df = self.data_manager.load_excel_data(team_file)
                
                if not team_df.empty:
                    st.write(f"**{len(team_df)} entries**")
                    st.dataframe(team_df, use_container_width=True)
                    
                    # Direct download button without intermediate step
                    excel_buffer = BytesIO()
                    team_df.to_excel(excel_buffer, index=False)
                    excel_buffer.seek(0)
                    
                    st.download_button(
                        label=f"📥 Download {team_name} Data",
                        data=excel_buffer.getvalue(),
                        file_name=f"{team_name}_efficiency_data_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=f"download_{team_name}",
                        use_container_width=True
                    )
                else:
                    st.info("No data entries yet.") 