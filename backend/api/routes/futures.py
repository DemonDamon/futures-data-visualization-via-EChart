from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from typing import Optional, List
from datetime import datetime
from models.futures import (
    FuturesDataResponse, 
    ChartDataRequest, 
    ChartDataResponse,
    UploadResponse
)
from services.futures_service import FuturesService

router = APIRouter()
futures_service = FuturesService()

@router.get("/data", response_model=FuturesDataResponse)
async def get_futures_data(
    instrument: Optional[str] = Query(None, description="合约代码"),
    start_time: Optional[datetime] = Query(None, description="开始时间"),
    end_time: Optional[datetime] = Query(None, description="结束时间"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(100, ge=1, le=1000, description="每页数量")
):
    """获取期货数据"""
    try:
        return await futures_service.get_futures_data(
            instrument=instrument,
            start_time=start_time,
            end_time=end_time,
            page=page,
            page_size=page_size
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chart-data", response_model=ChartDataResponse)
async def get_chart_data(request: ChartDataRequest):
    """获取图表数据"""
    try:
        return await futures_service.get_chart_data(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/instruments")
async def get_instruments():
    """获取所有合约代码"""
    try:
        return await futures_service.get_instruments()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload", response_model=UploadResponse)
async def upload_csv_file(file: UploadFile = File(...)):
    """上传CSV文件"""
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="只支持CSV文件")
        
        return await futures_service.upload_csv_file(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/data")
async def clear_data(instrument: Optional[str] = Query(None)):
    """清空数据"""
    try:
        return await futures_service.clear_data(instrument)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))