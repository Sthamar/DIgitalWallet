from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    KHALTI_PUBLIC_KEY: str = os.getenv("KHALTI_PUBLIC_KEY")
    KHALTI_SECRET_KEY: str = os.getenv("KHALTI_SECRET_KEY")
    KHALTI_API_BASE_URL:str = os.getenv("KHALTI_VERIFY_URL")
    
settings = Settings()