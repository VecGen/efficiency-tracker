"""
Data management classes for the Developer Efficiency Tracker
"""

import pandas as pd
import os
from openpyxl import Workbook
from .config import FILES, DEFAULT_SETTINGS, DB_COLUMNS


class DataManager:
    """Handles core data operations"""
    
    @staticmethod
    def create_empty_dataframe():
        """Create an empty DataFrame with the correct structure"""
        return pd.DataFrame(columns=DB_COLUMNS)
    
    @staticmethod
    def load_excel_data(file_path):
        """Load data from Excel file with backward compatibility"""
        if not os.path.exists(file_path):
            return DataManager.create_empty_dataframe()
        
        try:
            df = pd.read_excel(file_path)
            
            # Handle backward compatibility - convert old format to new format
            if 'Week' in df.columns and 'Week_Start' not in df.columns:
                # Convert old single Week column to Week_Start and Week_End
                df['Week_Start'] = pd.to_datetime(df['Week']).dt.date
                df['Week_End'] = df['Week_Start'] + pd.Timedelta(days=6)
                df = df.drop('Week', axis=1)
            
            # Ensure all required columns exist
            for col in DB_COLUMNS:
                if col not in df.columns:
                    df[col] = ''
            
            return df[DB_COLUMNS]  # Ensure column order
            
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return DataManager.create_empty_dataframe()
    
    @staticmethod
    def save_to_excel(df, file_path):
        """Save DataFrame to Excel file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else '.', exist_ok=True)
            
            # Save to Excel
            df.to_excel(file_path, index=False)
            return True
        except Exception as e:
            print(f"Error saving to {file_path}: {e}")
            return False


class TeamsConfigManager:
    """Manages team configuration data"""
    
    @staticmethod
    def load_teams_config():
        """Load teams configuration from Excel"""
        file_path = FILES['teams_config']
        
        if not os.path.exists(file_path):
            return {}
        
        try:
            df = pd.read_excel(file_path)
            teams_config = {}
            
            for _, row in df.iterrows():
                team_name = row['Team_Name']
                if team_name not in teams_config:
                    teams_config[team_name] = []
                
                if pd.notna(row.get('Developer_Name')):
                    # Check for both 'Link' and 'Access_Link' columns for backward compatibility
                    link = row.get('Access_Link', row.get('Link', ''))
                    
                    developer = {
                        'name': row['Developer_Name'],
                        'email': row.get('Email', ''),
                        'link': link
                    }
                    teams_config[team_name].append(developer)
            
            return teams_config
            
        except Exception as e:
            print(f"Error loading teams config: {e}")
            return {}
    
    @staticmethod
    def save_teams_config(teams_config):
        """Save teams configuration to Excel"""
        try:
            rows = []
            for team_name, developers in teams_config.items():
                if not developers:  # Empty team
                    rows.append({
                        'Team_Name': team_name,
                        'Developer_Name': '',
                        'Email': '',
                        'Access_Link': ''
                    })
                else:
                    for dev in developers:
                        rows.append({
                            'Team_Name': team_name,
                            'Developer_Name': dev['name'],
                            'Email': dev.get('email', ''),
                            'Access_Link': dev.get('link', '')
                        })
            
            df = pd.DataFrame(rows)
            df.to_excel(FILES['teams_config'], index=False)
            return True
            
        except Exception as e:
            print(f"Error saving teams config: {e}")
            return False


class TeamSettingsManager:
    """Manages team settings (categories and efficiency areas)"""
    
    @staticmethod
    def load_team_settings():
        """Load team settings from Excel"""
        file_path = FILES['team_settings']
        
        if not os.path.exists(file_path):
            # Return default settings if file doesn't exist
            default_settings = DEFAULT_SETTINGS.copy()
            default_settings['category_efficiency_mapping'] = {}
            return default_settings
        
        try:
            # Try to read from Excel
            df = pd.read_excel(file_path)
            
            settings = {
                'categories': [],
                'efficiency_areas': [],
                'category_efficiency_mapping': {}
            }
            
            # Extract categories
            if 'Categories' in df.columns:
                settings['categories'] = df['Categories'].dropna().tolist()
            
            # Extract efficiency areas
            if 'Efficiency_Areas' in df.columns:
                settings['efficiency_areas'] = df['Efficiency_Areas'].dropna().tolist()
            
            # Extract category efficiency mapping
            if 'Category_Mapping' in df.columns and 'Mapped_Areas' in df.columns:
                mapping_df = df[['Category_Mapping', 'Mapped_Areas']].dropna()
                for _, row in mapping_df.iterrows():
                    category = row['Category_Mapping']
                    areas_str = row['Mapped_Areas']
                    if areas_str and areas_str.strip():
                        # Split the comma-separated areas
                        areas = [area.strip() for area in areas_str.split(',') if area.strip()]
                        settings['category_efficiency_mapping'][category] = areas
                    else:
                        settings['category_efficiency_mapping'][category] = []
            
            # Use defaults if empty
            if not settings['categories']:
                settings['categories'] = DEFAULT_SETTINGS['categories'].copy()
            if not settings['efficiency_areas']:
                settings['efficiency_areas'] = DEFAULT_SETTINGS['efficiency_areas'].copy()
            
            return settings
            
        except Exception as e:
            print(f"Error loading team settings: {e}")
            default_settings = DEFAULT_SETTINGS.copy()
            default_settings['category_efficiency_mapping'] = {}
            return default_settings
    
    @staticmethod
    def save_team_settings(settings):
        """Save team settings to Excel"""
        try:
            # Calculate maximum length for padding
            mapping_data = settings.get('category_efficiency_mapping', {})
            max_len = max(
                len(settings['categories']), 
                len(settings['efficiency_areas']),
                len(mapping_data) if mapping_data else 0
            )
            
            # Pad lists to same length
            categories = settings['categories'] + [''] * (max_len - len(settings['categories']))
            efficiency_areas = settings['efficiency_areas'] + [''] * (max_len - len(settings['efficiency_areas']))
            
            # Prepare mapping data
            category_mapping = []
            mapped_areas = []
            
            for category, areas in mapping_data.items():
                category_mapping.append(category)
                mapped_areas.append(', '.join(areas) if areas else '')
            
            # Pad mapping data
            category_mapping += [''] * (max_len - len(category_mapping))
            mapped_areas += [''] * (max_len - len(mapped_areas))
            
            df = pd.DataFrame({
                'Categories': categories,
                'Efficiency_Areas': efficiency_areas,
                'Category_Mapping': category_mapping,
                'Mapped_Areas': mapped_areas
            })
            
            df.to_excel(FILES['team_settings'], index=False)
            return True
            
        except Exception as e:
            print(f"Error saving team settings: {e}")
            return False 