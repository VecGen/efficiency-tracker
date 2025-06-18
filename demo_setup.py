#!/usr/bin/env python3
"""
Demo Setup Script for Developer Efficiency Tracker

This script creates sample teams and developers to demonstrate the new two-tier system:
1. Admin interface for managers
2. Individual engineer links with access control
"""

import pandas as pd
import hashlib
import urllib.parse

def generate_engineer_link(developer_name, team_name, base_url="http://localhost:8501"):
    """Generate unique link for engineer"""
    params = {
        'dev': developer_name,
        'team': team_name,
        'token': hashlib.md5(f"{developer_name}_{team_name}".encode()).hexdigest()[:8]
    }
    query_string = urllib.parse.urlencode(params)
    return f"{base_url}/?{query_string}"

def create_team_settings():
    """Create default team settings file"""
    settings = {
        'categories': ['Feature Development', 'Bug Fix', 'Code Refactoring', 'Documentation', 'Testing', 'Code Review'],
        'efficiency_areas': ['Code Generation', 'Bug Fixing', 'Documentation Writing', 'Test Creation', 'Code Refactoring', 'API Integration', 'Database Queries', 'Learning New Concepts']
    }
    
    settings_file = "team_settings.xlsx"
    
    with pd.ExcelWriter(settings_file, engine='openpyxl') as writer:
        # Save categories
        cat_df = pd.DataFrame({'Category': settings['categories']})
        cat_df.to_excel(writer, sheet_name='Categories', index=False)
        
        # Save efficiency areas
        area_df = pd.DataFrame({'Area': settings['efficiency_areas']})
        area_df.to_excel(writer, sheet_name='Efficiency_Areas', index=False)
    
    print(f"✅ Team settings saved to {settings_file}")
    print(f"   📋 Categories: {len(settings['categories'])}")
    print(f"   🎯 Efficiency Areas: {len(settings['efficiency_areas'])}")
    
    return settings

def get_week_dates(date):
    """Get Monday and Sunday of the week containing the given date"""
    from datetime import timedelta
    days_since_monday = date.weekday()
    monday = date - timedelta(days=days_since_monday)
    sunday = monday + timedelta(days=6)
    return monday, sunday

def create_demo_teams():
    """Create demo teams configuration"""
    
    # Demo teams and developers
    teams_data = {
        'Frontend Team': [
            {'name': 'Alice Johnson', 'email': 'alice.johnson@company.com'},
            {'name': 'Bob Smith', 'email': 'bob.smith@company.com'},
            {'name': 'Carol Davis', 'email': 'carol.davis@company.com'}
        ],
        'Backend Team': [
            {'name': 'David Wilson', 'email': 'david.wilson@company.com'},
            {'name': 'Eve Chen', 'email': 'eve.chen@company.com'},
            {'name': 'Frank Miller', 'email': 'frank.miller@company.com'}
        ],
        'Platform Team': [
            {'name': 'Grace Lee', 'email': 'grace.lee@company.com'},
            {'name': 'Henry Taylor', 'email': 'henry.taylor@company.com'}
        ]
    }
    
    # Create teams configuration with links
    config_data = []
    
    print("🚀 Creating Demo Teams Configuration")
    print("=" * 50)
    
    for team_name, developers in teams_data.items():
        print(f"\n🏢 {team_name}:")
        
        for dev in developers:
            link = generate_engineer_link(dev['name'], team_name)
            config_data.append({
                'Team_Name': team_name,
                'Developer_Name': dev['name'],
                'Email': dev['email'],
                'Link': link
            })
            
            print(f"  👤 {dev['name']}")
            print(f"     📧 {dev['email']}")
            print(f"     🔗 {link}")
    
    # Save to Excel
    df = pd.DataFrame(config_data)
    config_file = "teams_config.xlsx"
    df.to_excel(config_file, index=False)
    
    print(f"\n✅ Teams configuration saved to {config_file}")
    return config_data

def create_sample_data():
    """Create some sample efficiency data for demo"""
    
    from datetime import datetime, timedelta
    import random
    
    # Sample data for different teams
    sample_entries = []
    
    teams = {
        'Frontend Team': ['Alice Johnson', 'Bob Smith', 'Carol Davis'],
        'Backend Team': ['David Wilson', 'Eve Chen', 'Frank Miller'],
        'Platform Team': ['Grace Lee', 'Henry Taylor']
    }
    
    categories = ['Feature Development', 'Bug Fix', 'Code Refactoring', 'Documentation', 'Testing', 'Code Review']
    areas = ['Code Generation', 'Bug Fixing', 'Documentation Writing', 'Test Creation', 'Code Refactoring', 'API Integration', 'Database Queries', 'Learning New Concepts']
    
    print("\n📊 Creating Sample Efficiency Data")
    print("=" * 40)
    
    for team_name, developers in teams.items():
        team_entries = []
        
        for dev_name in developers:
            # Create 3-5 entries per developer
            num_entries = random.randint(3, 5)
            
            for i in range(num_entries):
                # Random date in last 4 weeks
                days_ago = random.randint(1, 28)
                entry_date = datetime.now().date() - timedelta(days=days_ago)
                
                # Get week start and end dates
                week_start, week_end = get_week_dates(entry_date)
                
                # Random but realistic values
                original_estimate = round(random.uniform(2, 12), 1)
                efficiency_gained = round(original_estimate * random.uniform(0.15, 0.4), 1)
                
                # Random selection of 1-3 efficiency areas
                selected_areas = random.sample(areas, random.randint(1, 3))
                
                entry = {
                    'Week_Start': week_start.strftime('%Y-%m-%d'),
                    'Week_End': week_end.strftime('%Y-%m-%d'),
                    'Story_ID': f"ENG-{random.randint(1000, 9999)}",
                    'Developer_Name': dev_name,
                    'Team_Name': team_name,
                    'Original_Estimate_Hours': original_estimate,
                    'Efficiency_Gained_Hours': efficiency_gained,
                    'Copilot_Used': random.choice(['Yes', 'Yes', 'Yes', 'No']),  # 75% yes
                    'Category': random.choice(categories),
                    'Areas_of_Efficiency': ', '.join(selected_areas),
                    'Notes_Observations': random.choice([
                        'Copilot generated the entire function with proper error handling',
                        'Helped with complex regex pattern and validation logic',
                        'Auto-completed API integration with authentication',
                        'Suggested better error handling and logging approach',
                        'Generated comprehensive unit tests with edge cases',
                        'Improved algorithm efficiency and reduced complexity',
                        'Assisted with database query optimization',
                        'Generated documentation and code comments automatically'
                    ])
                }
                
                team_entries.append(entry)
        
        # Save team data to separate Excel file
        team_df = pd.DataFrame(team_entries)
        safe_team_name = team_name.replace(' ', '_').replace('/', '_')
        team_file = f"efficiency_data_{safe_team_name}.xlsx"
        
        with pd.ExcelWriter(team_file, engine='openpyxl') as writer:
            team_df.to_excel(writer, index=False, sheet_name='Efficiency_Data')
        
        total_time_saved = team_df['Efficiency_Gained_Hours'].sum()
        avg_efficiency = (team_df['Efficiency_Gained_Hours'] / team_df['Original_Estimate_Hours'] * 100).mean()
        
        print(f"  🏢 {team_name}: {len(team_entries)} entries, {total_time_saved:.1f}h saved, {avg_efficiency:.1f}% avg efficiency")
    
    print(f"\n✅ Sample data created for all teams")

def print_usage_instructions():
    """Print instructions for using the demo"""
    
    print("\n" + "=" * 60)
    print("🎯 HOW TO USE THE DEMO")
    print("=" * 60)
    
    print("\n1️⃣ START THE APPLICATION:")
    print("   python -m streamlit run app.py")
    
    print("\n2️⃣ ADMIN ACCESS (Default):")
    print("   • Open http://localhost:8501")
    print("   • You'll see the Admin Panel")
    print("   • Navigate between Team Setup, Team Settings, Dashboard, Data Management")
    
    print("\n3️⃣ ENGINEER ACCESS (Individual Links):")
    print("   • Copy any engineer link from the Team Setup page")
    print("   • Example links created:")
    
    # Show a few example links
    examples = [
        ('Alice Johnson', 'Frontend Team'),
        ('David Wilson', 'Backend Team'),
        ('Grace Lee', 'Platform Team')
    ]
    
    for name, team in examples:
        link = generate_engineer_link(name, team)
        print(f"   • {name}: {link}")
    
    print("\n4️⃣ KEY DIFFERENCES:")
    print("   ✅ Admin Panel:")
    print("      - Setup teams and developers")
    print("      - Configure task categories and efficiency areas")
    print("      - View cross-team analytics")
    print("      - Export all data")
    print("      - Generate engineer links")
    
    print("   ✅ Engineer Interface:")
    print("      - Simplified weekly update form")
    print("      - Week-based data entry (current/past weeks only)")
    print("      - Multiple efficiency area selection (checkboxes)")
    print("      - Personal dashboard")
    print("      - Only see own data")
    print("      - Pre-populated name and team")
    
    print("\n5️⃣ NEW FEATURES:")
    print("   📅 Week-based Updates:")
    print("      - Current week pre-selected")
    print("      - Can log for past weeks, not future")
    print("      - Clear week range display")
    
    print("   ☑️ Multiple Efficiency Areas:")
    print("      - Checkbox selection instead of dropdown")
    print("      - Select multiple areas where Copilot helped")
    print("      - Configurable by team managers")
    
    print("   ⚙️ Team Settings:")
    print("      - Managers can customize categories")
    print("      - Managers can customize efficiency areas")
    print("      - Settings apply to all team engineers")
    
    print("\n6️⃣ DATA SEPARATION:")
    print("   • Each team has its own Excel file")
    print("   • Engineers only access their team's data")
    print("   • Admins can view all teams combined")
    
    print("\n7️⃣ SECURITY:")
    print("   • Engineer links contain access tokens")
    print("   • No cross-team data visibility")
    print("   • Invalid tokens are rejected")

def main():
    """Main demo setup function"""
    
    print("🚀 DEVELOPER EFFICIENCY TRACKER - DEMO SETUP")
    print("=" * 60)
    print("Setting up demo teams, developers, settings, and sample data...")
    
    # Create team settings
    create_team_settings()
    
    # Create teams configuration
    create_demo_teams()
    
    # Create sample efficiency data
    create_sample_data()
    
    # Print usage instructions
    print_usage_instructions()
    
    print("\n🎉 Demo setup complete!")
    print("Run 'python -m streamlit run app.py' to start the application.")

if __name__ == "__main__":
    main() 