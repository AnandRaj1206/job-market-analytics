from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/jobmarket"
    adzuna_app_id: str = ""
    adzuna_app_key: str = ""
    groq_api_key: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
