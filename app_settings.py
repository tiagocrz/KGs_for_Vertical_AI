"""
Centralized settings file for KGs_for_Vertical_AI project.
All environment variables are loaded here and imported by other modules.
"""
import os
from pathlib import Path
from dotenv import load_dotenv
PROJECT_ROOT = Path(__file__).resolve().parent
env_path = PROJECT_ROOT / '.env'
print("Project root path:", PROJECT_ROOT)
load_dotenv(env_path, override=True)

#check if the loading was successful
if not os.getenv("AZURE_OPENAI_API_KEY"):
    raise ValueError("Failed to load environment variables from .env file")
else:
    print(os.getenv("AZURE_OPENAI_API_KEY")[:5] + "..." )  # Print first 5 characters of the key for verification
    print("Environment variables loaded successfully")

# Azure OpenAI settings
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

# Azure OpenAI model deployments
AZURE_DEPLOYMENT_GPT41 = os.getenv("AZURE_DEPLOYMENT_GPT41")
AZURE_DEPLOYMENT_GPT41_NANO = os.getenv("AZURE_DEPLOYMENT_GPT41_NANO")

# Groq API settings
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TESTE = "123"