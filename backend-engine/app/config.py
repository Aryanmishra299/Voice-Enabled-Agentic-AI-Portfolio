# Pydantic environment configurations & variable typing

from pydantic_settings import BaseSettings
from pydantic import Field
import os

class Settings(BaseSettings):
    """
    Validates and locks system configuration states at startup.
    Ensures safe, type-hinted environments for inference calls.
    """
    PORT: int = Field(default=8000, description="Server port listener allocation")
    HOST: str = Field(default="127.0.0.1", description="Server interface allocation hook")
    GROQ_API_KEY: str = Field(..., description="Secret operational token for Groq LLaMA reasoning access")
    ENVIRONMENT: str = Field(default="development", description="Current deployment workspace state")

    class Config:
        # Pulls parameters directly from your secure local environment matrix file
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        env_file_encoding = "utf-8"

# Instantiate a single global config system reference node
settings = Settings()
