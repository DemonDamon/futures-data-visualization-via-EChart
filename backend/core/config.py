from pydantic_settings import BaseSettings
from typing import List
from pydantic import field_validator

class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "期货数据可视化API"
    DEBUG: bool = True
    
    # Supabase配置
    SUPABASE_URL: str = "https://qlqjqwqjqwqjqwqjqwqj.supabase.co"
    SUPABASE_ANON_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFscWpxd3FqcXdxanF3cWpxd3FqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU3MzE2MDAsImV4cCI6MjA1MTMwNzYwMH0.dummy_anon_key_for_demo"
    SUPABASE_SERVICE_ROLE_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFscWpxd3FqcXdxanF3cWpxd3FqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczNTczMTYwMCwiZXhwIjoyMDUxMzA3NjAwfQ.dummy_service_role_key_for_demo"
    
    # 数据库配置
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "futures_data"
    
    # CORS配置
    ALLOWED_HOSTS: str = "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173"
    
    @field_validator('ALLOWED_HOSTS')
    @classmethod
    def parse_allowed_hosts(cls, v):
        if isinstance(v, str):
            return [host.strip() for host in v.split(',')]
        return v
    
    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # JWT配置
    JWT_SECRET_KEY: str = "your-secret-key-here"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()