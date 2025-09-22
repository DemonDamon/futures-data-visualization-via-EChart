from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from typing import List, Optional
import pandas as pd
import io
from datetime import datetime
from models.schemas import (
    DatasetCreate, DatasetResponse, KlineDataCreate, KlineDataResponse,
    FileUploadResponse, MessageResponse
)
from core.database import get_supabase_client
from api.auth import get_current_user_dependency

router = APIRouter(prefix="/data", tags=["数据管理"])

@router.post("/datasets", response_model=DatasetResponse)
async def create_dataset(
    dataset: DatasetCreate,
    current_user: dict = Depends(get_current_user_dependency)
):
    """创建数据集"""
    supabase = get_supabase_client()
    
    try:
        new_dataset = {
            "name": dataset.name,
            "description": dataset.description,
            "symbol": dataset.symbol,
            "timeframe": dataset.timeframe,
            "user_id": current_user['id']
        }
        
        result = supabase.table('datasets').insert(new_dataset).execute()
        
        if result.data:
            dataset_data = result.data[0]
            return DatasetResponse(
                id=dataset_data['id'],
                name=dataset_data['name'],
                description=dataset_data['description'],
                symbol=dataset_data['symbol'],
                timeframe=dataset_data['timeframe'],
                user_id=dataset_data['user_id'],
                created_at=dataset_data['created_at'],
                updated_at=dataset_data['updated_at']
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="创建数据集失败"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建数据集时发生错误: {str(e)}"
        )

@router.get("/datasets", response_model=List[DatasetResponse])
async def get_datasets(
    current_user: dict = Depends(get_current_user_dependency)
):
    """获取用户的数据集列表"""
    supabase = get_supabase_client()
    
    try:
        result = supabase.table('datasets').select('*').eq('user_id', current_user['id']).execute()
        
        datasets = []
        for dataset in result.data:
            datasets.append(DatasetResponse(
                id=dataset['id'],
                name=dataset['name'],
                description=dataset['description'],
                symbol=dataset['symbol'],
                timeframe=dataset['timeframe'],
                user_id=dataset['user_id'],
                created_at=dataset['created_at'],
                updated_at=dataset['updated_at']
            ))
        
        return datasets
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取数据集列表失败: {str(e)}"
        )

@router.post("/upload-csv", response_model=FileUploadResponse)
async def upload_csv_file(
    file: UploadFile = File(...),
    dataset_id: Optional[str] = None,
    current_user: dict = Depends(get_current_user_dependency)
):
    """上传CSV文件并解析K线数据"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只支持CSV文件格式"
        )
    
    try:
        # 读取CSV文件
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # 验证CSV格式（期望包含：timestamp, open, high, low, close, volume列）
        required_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"CSV文件必须包含以下列: {', '.join(required_columns)}"
            )
        
        supabase = get_supabase_client()
        
        # 如果提供了dataset_id，验证数据集是否存在且属于当前用户
        if dataset_id:
            dataset_result = supabase.table('datasets').select('*').eq('id', dataset_id).eq('user_id', current_user['id']).execute()
            if not dataset_result.data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="数据集不存在或无权限访问"
                )
        
        # 准备K线数据
        kline_data = []
        for _, row in df.iterrows():
            kline_record = {
                "dataset_id": dataset_id,
                "timestamp": pd.to_datetime(row['timestamp']).isoformat(),
                "open_price": float(row['open']),
                "high_price": float(row['high']),
                "low_price": float(row['low']),
                "close_price": float(row['close']),
                "volume": float(row['volume'])
            }
            kline_data.append(kline_record)
        
        # 批量插入K线数据
        if kline_data:
            result = supabase.table('kline_data').insert(kline_data).execute()
            if not result.data:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="K线数据插入失败"
                )
        
        return FileUploadResponse(
            filename=file.filename,
            file_size=len(contents),
            upload_time=datetime.now(),
            dataset_id=dataset_id
        )
        
    except pd.errors.EmptyDataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CSV文件为空"
        )
    except pd.errors.ParserError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CSV文件格式错误"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件上传处理失败: {str(e)}"
        )

@router.get("/kline/{dataset_id}", response_model=List[KlineDataResponse])
async def get_kline_data(
    dataset_id: str,
    limit: int = 1000,
    current_user: dict = Depends(get_current_user_dependency)
):
    """获取K线数据"""
    supabase = get_supabase_client()
    
    try:
        # 验证数据集权限
        dataset_result = supabase.table('datasets').select('*').eq('id', dataset_id).eq('user_id', current_user['id']).execute()
        if not dataset_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="数据集不存在或无权限访问"
            )
        
        # 获取K线数据
        result = supabase.table('kline_data').select('*').eq('dataset_id', dataset_id).order('timestamp').limit(limit).execute()
        
        kline_data = []
        for data in result.data:
            kline_data.append(KlineDataResponse(
                id=data['id'],
                dataset_id=data['dataset_id'],
                timestamp=data['timestamp'],
                open_price=data['open_price'],
                high_price=data['high_price'],
                low_price=data['low_price'],
                close_price=data['close_price'],
                volume=data['volume']
            ))
        
        return kline_data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取K线数据失败: {str(e)}"
        )

@router.delete("/datasets/{dataset_id}", response_model=MessageResponse)
async def delete_dataset(
    dataset_id: str,
    current_user: dict = Depends(get_current_user_dependency)
):
    """删除数据集"""
    supabase = get_supabase_client()
    
    try:
        # 验证数据集权限
        dataset_result = supabase.table('datasets').select('*').eq('id', dataset_id).eq('user_id', current_user['id']).execute()
        if not dataset_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="数据集不存在或无权限访问"
            )
        
        # 删除相关的K线数据
        supabase.table('kline_data').delete().eq('dataset_id', dataset_id).execute()
        
        # 删除数据集
        result = supabase.table('datasets').delete().eq('id', dataset_id).execute()
        
        return MessageResponse(message="数据集删除成功")
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除数据集失败: {str(e)}"
        )