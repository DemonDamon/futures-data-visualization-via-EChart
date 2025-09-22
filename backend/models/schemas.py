from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# 用户相关模型
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    created_at: datetime
    updated_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    user: Optional[Dict[str, Any]] = None

# 数据集相关模型
class DatasetCreate(BaseModel):
    name: str
    description: Optional[str] = None
    symbol: str
    timeframe: str

class DatasetResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    symbol: str
    timeframe: str
    user_id: str
    created_at: datetime
    updated_at: datetime

# K线数据模型
class KlineData(BaseModel):
    timestamp: datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float

class KlineDataCreate(BaseModel):
    dataset_id: str
    data: List[KlineData]

class KlineDataResponse(BaseModel):
    id: str
    dataset_id: str
    timestamp: datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float

# 图表配置模型
class ChartConfigCreate(BaseModel):
    name: str
    config: Dict[str, Any]
    is_default: bool = False

class ChartConfigResponse(BaseModel):
    id: str
    name: str
    config: Dict[str, Any]
    is_default: bool
    user_id: str
    created_at: datetime
    updated_at: datetime

# 文件上传模型
class FileUploadResponse(BaseModel):
    filename: str
    file_size: int
    upload_time: datetime
    dataset_id: Optional[str] = None

# 通用响应模型
class MessageResponse(BaseModel):
    message: str
    success: bool = True

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    success: bool = False