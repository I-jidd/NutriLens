import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "NutriLens"
    GEMINI_API_KEY: str
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        # This allows loading from the parent directory if running from root
        env_file_encoding = 'utf-8'

# Create a global settings object
# We use a try-except block to handle cases where .env might be missing during initial setup
try:
    settings = Settings()
except Exception as e:
    print(f"WARNING: Could not load settings from .env file. Ensure GEMINI_API_KEY is set in environment. Error: {e}")
    # Fallback for development if needed, though production should fail if keys are missing
    settings = None