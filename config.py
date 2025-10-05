"""Configuration settings for the Instagram Advertisement Agent."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the Instagram Advertisement Agent."""
    
    # Cerebrus API Configuration
    CEREBRUS_API_KEY = os.getenv('CEREBRUS_API_KEY')
    CEREBRUS_BASE_URL = os.getenv('CEREBRUS_BASE_URL', 'https://api.cerebrus.com')
    
    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Instagram API Configuration
    INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')
    INSTAGRAM_APP_ID = os.getenv('INSTAGRAM_APP_ID')
    INSTAGRAM_APP_SECRET = os.getenv('INSTAGRAM_APP_SECRET')
    
    # Storage Configuration
    STORAGE_PATH = os.getenv('STORAGE_PATH', './data')
    
    # Scheduling Configuration
    POST_TIME = "00:00"  # 12 AM daily
    
    # Content Configuration
    MAX_CAPTION_LENGTH = 2200
    MAX_HASHTAGS = 30
    
    @classmethod
    def validate(cls):
        """Validate that all required configuration is present."""
        required_vars = [
            'CEREBRUS_API_KEY',
            'GEMINI_API_KEY',
            'INSTAGRAM_ACCESS_TOKEN',
            'INSTAGRAM_APP_ID',
            'INSTAGRAM_APP_SECRET'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True