"""
S3-compatible data manager for the Developer Efficiency Tracker
Provides cloud storage capabilities with fallback to local storage
"""

import pandas as pd
import logging
from datetime import datetime

# Try to import boto3, fallback to local storage if not available
try:
    import boto3
    from botocore.exceptions import ClientError, NoCredentialsError
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False
    logging.warning("boto3 not available, falling back to local storage")

from .config import AWS_CONFIG, FILES, DB_COLUMNS, DEFAULT_SETTINGS
from .data_manager import DataManager, TeamsConfigManager, TeamSettingsManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class S3DataManager:
    """Handles data operations with AWS S3 storage"""
    
    def __init__(self):
        if not BOTO3_AVAILABLE:
            raise ImportError("boto3 is required for S3 operations")
            
        self.bucket_name = AWS_CONFIG['bucket_name']
        self.region = AWS_CONFIG['region']
        
        try:
            self.s3_client = boto3.client('s3', region_name=self.region)
            self._ensure_bucket_exists()
            logger.info(f"S3DataManager initialized with bucket: {self.bucket_name}")
        except (NoCredentialsError, ClientError) as e:
            logger.error(f"Failed to initialize S3 client: {e}")
            raise
    
    def _ensure_bucket_exists(self):
        """Ensure the S3 bucket exists, create if it doesn't"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            logger.info(f"Bucket {self.bucket_name} exists")
        except ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                try:
                    if self.region == 'us-east-1':
                        self.s3_client.create_bucket(Bucket=self.bucket_name)
                    else:
                        self.s3_client.create_bucket(
                            Bucket=self.bucket_name,
                            CreateBucketConfiguration={'LocationConstraint': self.region}
                        )
                    logger.info(f"Created bucket: {self.bucket_name}")
                except ClientError as create_error:
                    logger.error(f"Failed to create bucket: {create_error}")
                    raise
            else:
                logger.error(f"Error accessing bucket: {e}")
                raise
    
    def create_empty_dataframe(self):
        """Create an empty DataFrame with the correct structure"""
        return pd.DataFrame(columns=[
            'Week_Start', 'Week_End', 'Story_ID', 'Developer_Name', 'Team_Name',
            'Original_Estimate_Hours', 'Efficiency_Gained_Hours', 'Copilot_Used',
            'Category', 'Areas_of_Efficiency', 'Notes_Observations'
        ])
    
    def load_excel_data(self, filename):
        """Load data from Excel file in S3"""
        try:
            # Check if file exists
            if not self.file_exists(filename):
                logger.info(f"File {filename} doesn't exist, returning empty DataFrame")
                return self.create_empty_dataframe()
            
            # Download file from S3
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=filename)
            df = pd.read_excel(response['Body'])
            
            # Handle backward compatibility for old data formats
            if 'Week' in df.columns and 'Week_Start' not in df.columns:
                df['Week_Start'] = df['Week']
                df['Week_End'] = df['Week']  # For old data, use same date
            
            # Ensure all required columns exist
            expected_columns = self.create_empty_dataframe().columns
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = ''
            
            logger.info(f"Loaded {len(df)} rows from {filename}")
            return df
            
        except ClientError as e:
            logger.error(f"Error loading data from S3: {e}")
            return self.create_empty_dataframe()
        except Exception as e:
            logger.error(f"Unexpected error loading data: {e}")
            return self.create_empty_dataframe()
    
    def save_to_excel(self, df, filename):
        """Save DataFrame to Excel file in S3"""
        try:
            # Create Excel file in memory
            from io import BytesIO
            excel_buffer = BytesIO()
            
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Efficiency_Data')
            
            # Upload to S3
            excel_buffer.seek(0)
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=excel_buffer.getvalue(),
                ContentType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
            logger.info(f"Saved {len(df)} rows to {filename} in S3")
            return True
            
        except ClientError as e:
            logger.error(f"Error saving data to S3: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error saving data: {e}")
            return False
    
    def file_exists(self, filename):
        """Check if a file exists in S3"""
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=filename)
            return True
        except ClientError:
            return False
    
    def list_team_files(self):
        """List all team data files in S3"""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix='efficiency_data_'
            )
            
            if 'Contents' in response:
                return [obj['Key'] for obj in response['Contents'] 
                       if obj['Key'].endswith('.xlsx')]
            return []
            
        except ClientError as e:
            logger.error(f"Error listing team files: {e}")
            return []


class S3TeamsConfigManager:
    """Manages team configuration data in S3"""
    
    def __init__(self):
        if not BOTO3_AVAILABLE:
            raise ImportError("boto3 is required for S3 operations")
            
        self.bucket_name = AWS_CONFIG['bucket_name']
        self.config_file = 'teams_config.json'
        self.s3_client = boto3.client('s3', region_name=AWS_CONFIG['region'])
    
    def load_teams_config(self):
        """Load teams configuration from S3"""
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=self.config_file)
            import json
            config = json.loads(response['Body'].read().decode('utf-8'))
            logger.info(f"Loaded teams config from S3")
            return config
        except ClientError:
            logger.info("Teams config not found in S3, returning empty config")
            return {}
        except Exception as e:
            logger.error(f"Error loading teams config: {e}")
            return {}
    
    def save_teams_config(self, config):
        """Save teams configuration to S3"""
        try:
            import json
            config_json = json.dumps(config, indent=2)
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=self.config_file,
                Body=config_json,
                ContentType='application/json'
            )
            logger.info("Saved teams config to S3")
            return True
        except Exception as e:
            logger.error(f"Error saving teams config: {e}")
            return False


class S3TeamSettingsManager:
    """Manages team settings in S3"""
    
    def __init__(self):
        if not BOTO3_AVAILABLE:
            raise ImportError("boto3 is required for S3 operations")
            
        self.bucket_name = AWS_CONFIG['bucket_name']
        self.settings_file = 'team_settings.json'
        self.s3_client = boto3.client('s3', region_name=AWS_CONFIG['region'])
    
    def load_team_settings(self):
        """Load team settings from S3"""
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=self.settings_file)
            import json
            settings = json.loads(response['Body'].read().decode('utf-8'))
            logger.info("Loaded team settings from S3")
            return settings
        except ClientError:
            logger.info("Team settings not found in S3, returning default settings")
            return self._get_default_settings()
        except Exception as e:
            logger.error(f"Error loading team settings: {e}")
            return self._get_default_settings()
    
    def save_team_settings(self, settings):
        """Save team settings to S3"""
        try:
            import json
            settings_json = json.dumps(settings, indent=2)
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=self.settings_file,
                Body=settings_json,
                ContentType='application/json'
            )
            logger.info("Saved team settings to S3")
            return True
        except Exception as e:
            logger.error(f"Error saving team settings: {e}")
            return False
    
    def _get_default_settings(self):
        """Get default team settings"""
        return {
            'categories': [
                'Feature Development', 'Bug Fixes', 'Code Review', 'Testing',
                'Documentation', 'Refactoring', 'API Development', 'Database Work'
            ],
            'efficiency_areas': [
                'Code Generation', 'Debugging', 'API Design', 'Test Writing',
                'Code Completion', 'Documentation', 'Refactoring', 'Code Analysis',
                'Query Optimization', 'Test Data Creation'
            ],
            'category_efficiency_mapping': {}
        }


# Factory functions to get the appropriate data manager
def get_data_manager():
    """Get the appropriate data manager based on configuration"""
    if AWS_CONFIG['use_s3'] and BOTO3_AVAILABLE:
        try:
            return S3DataManager()
        except Exception as e:
            logger.warning(f"Failed to initialize S3DataManager, falling back to local: {e}")
            return DataManager()
    else:
        return DataManager()


def get_teams_config_manager():
    """Get the appropriate teams config manager based on configuration"""
    if AWS_CONFIG['use_s3'] and BOTO3_AVAILABLE:
        try:
            return S3TeamsConfigManager()
        except Exception as e:
            logger.warning(f"Failed to initialize S3TeamsConfigManager, falling back to local: {e}")
            return TeamsConfigManager()
    else:
        return TeamsConfigManager()


def get_team_settings_manager():
    """Get the appropriate team settings manager based on configuration"""
    if AWS_CONFIG['use_s3'] and BOTO3_AVAILABLE:
        try:
            return S3TeamSettingsManager()
        except Exception as e:
            logger.warning(f"Failed to initialize S3TeamSettingsManager, falling back to local: {e}")
            return TeamSettingsManager()
    else:
        return TeamSettingsManager() 