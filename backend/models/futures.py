from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class FuturesData(BaseModel):
    """期货数据模型"""
    instrument: str = Field(..., description="合约代码")
    time: datetime = Field(..., description="时间")
    interface: str = Field(..., description="接口类型")
    open: float = Field(..., description="开盘价")
    high: float = Field(..., description="最高价")
    low: float = Field(..., description="最低价")
    close: float = Field(..., description="收盘价")
    volume: int = Field(..., description="成交量")
    open_interest: Optional[int] = Field(None, description="持仓量")
    
class FuturesDataResponse(BaseModel):
    """期货数据响应模型"""
    data: List[FuturesData]
    total: int
    page: int
    page_size: int
    
class ChartDataRequest(BaseModel):
    """图表数据请求模型"""
    instrument: str = Field(..., description="合约代码")
    start_time: Optional[datetime] = Field(None, description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")
    interval: str = Field("5m", description="时间间隔")
    
class ChartDataResponse(BaseModel):
    """图表数据响应模型"""
    instrument: str
    data: List[List[float]]  # [timestamp, open, close, low, high, volume]
    
class UploadResponse(BaseModel):
    """文件上传响应模型"""
    message: str
    filename: str
    records_count: int