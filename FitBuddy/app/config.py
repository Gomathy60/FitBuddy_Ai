import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent/'.env')
class Settings:
 APP_NAME=os.getenv('APP_NAME','FitBuddy'); DATABASE_URL=os.getenv('DATABASE_URL','sqlite:///./fitbuddy.db')
 GEMINI_API_KEY=os.getenv('GEMINI_API_KEY',''); GEMINI_WORKOUT_MODEL=os.getenv('GEMINI_WORKOUT_MODEL','gemini-3.8-flash'); GEMINI_TIP_MODEL=os.getenv('GEMINI_TIP_MODEL','gemini-3.8-flash'); ADMIN_KEY=os.getenv('ADMIN_KEY','fitbuddy-admin-123')
settings=Settings()
