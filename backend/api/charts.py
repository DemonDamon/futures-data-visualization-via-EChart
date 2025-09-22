from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from models.schemas import (
    ChartConfigCreate, ChartConfigResponse, MessageResponse
)
from core.database import get_supabase_client
from api.auth import get_current_user_dependency

router = APIRouter(prefix="/charts", tags=["图表配置"])

@router.post("/configs", response_model=ChartConfigResponse)
async def create_chart_config(
    config: ChartConfigCreate,
    current_user: dict = Depends(get_current_user_dependency)
):
    """创建图表配置"""
    supabase = get_supabase_client()
    
    try:
        new_config = {
            "name": config.name,
            "config": config.config,
            "is_default": config.is_default,
            "user_id": current_user['id']
        }
        
        result = supabase.table('chart_configs').insert(new_config).execute()
        
        if result.data:
            config_data = result.data[0]
            return ChartConfigResponse(
                id=config_data['id'],
                name=config_data['name'],
                config=config_data['config'],
                is_default=config_data['is_default'],
                user_id=config_data['user_id'],
                created_at=config_data['created_at'],
                updated_at=config_data['updated_at']
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="创建图表配置失败"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建图表配置时发生错误: {str(e)}"
        )

@router.get("/configs", response_model=List[ChartConfigResponse])
async def get_chart_configs(
    current_user: dict = Depends(get_current_user_dependency)
):
    """获取用户的图表配置列表"""
    supabase = get_supabase_client()
    
    try:
        result = supabase.table('chart_configs').select('*').eq('user_id', current_user['id']).execute()
        
        configs = []
        for config in result.data:
            configs.append(ChartConfigResponse(
                id=config['id'],
                name=config['name'],
                config=config['config'],
                is_default=config['is_default'],
                user_id=config['user_id'],
                created_at=config['created_at'],
                updated_at=config['updated_at']
            ))
        
        return configs
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取图表配置列表失败: {str(e)}"
        )

@router.get("/configs/default", response_model=ChartConfigResponse)
async def get_default_chart_config(
    current_user: dict = Depends(get_current_user_dependency)
):
    """获取默认图表配置"""
    supabase = get_supabase_client()
    
    try:
        # 先查找用户的默认配置
        result = supabase.table('chart_configs').select('*').eq('user_id', current_user['id']).eq('is_default', True).execute()
        
        if result.data:
            config = result.data[0]
            return ChartConfigResponse(
                id=config['id'],
                name=config['name'],
                config=config['config'],
                is_default=config['is_default'],
                user_id=config['user_id'],
                created_at=config['created_at'],
                updated_at=config['updated_at']
            )
        else:
            # 如果没有默认配置，返回系统默认配置
            default_config = {
                "title": {
                    "text": "期货K线图",
                    "left": "center"
                },
                "tooltip": {
                    "trigger": "axis",
                    "axisPointer": {
                        "type": "cross"
                    }
                },
                "legend": {
                    "data": ["K线", "成交量"],
                    "top": 30
                },
                "grid": [
                    {
                        "left": "10%",
                        "right": "8%",
                        "height": "50%"
                    },
                    {
                        "left": "10%",
                        "right": "8%",
                        "top": "70%",
                        "height": "16%"
                    }
                ],
                "xAxis": [
                    {
                        "type": "category",
                        "data": [],
                        "scale": True,
                        "boundaryGap": False,
                        "axisLine": {"onZero": False},
                        "splitLine": {"show": False},
                        "min": "dataMin",
                        "max": "dataMax"
                    },
                    {
                        "type": "category",
                        "gridIndex": 1,
                        "data": [],
                        "scale": True,
                        "boundaryGap": False,
                        "axisLine": {"onZero": False},
                        "axisTick": {"show": False},
                        "splitLine": {"show": False},
                        "axisLabel": {"show": False},
                        "min": "dataMin",
                        "max": "dataMax"
                    }
                ],
                "yAxis": [
                    {
                        "scale": True,
                        "splitArea": {
                            "show": True
                        }
                    },
                    {
                        "scale": True,
                        "gridIndex": 1,
                        "splitNumber": 2,
                        "axisLabel": {"show": False},
                        "axisLine": {"show": False},
                        "axisTick": {"show": False},
                        "splitLine": {"show": False}
                    }
                ],
                "dataZoom": [
                    {
                        "type": "inside",
                        "xAxisIndex": [0, 1],
                        "start": 50,
                        "end": 100
                    },
                    {
                        "show": True,
                        "xAxisIndex": [0, 1],
                        "type": "slider",
                        "top": "90%",
                        "start": 50,
                        "end": 100
                    }
                ],
                "series": [
                    {
                        "name": "K线",
                        "type": "candlestick",
                        "data": [],
                        "itemStyle": {
                            "color": "#ec0000",
                            "color0": "#00da3c",
                            "borderColor": "#8A0000",
                            "borderColor0": "#008F28"
                        }
                    },
                    {
                        "name": "成交量",
                        "type": "bar",
                        "xAxisIndex": 1,
                        "yAxisIndex": 1,
                        "data": []
                    }
                ]
            }
            
            return ChartConfigResponse(
                id="default",
                name="系统默认配置",
                config=default_config,
                is_default=True,
                user_id=current_user['id'],
                created_at="2024-01-01T00:00:00",
                updated_at="2024-01-01T00:00:00"
            )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取默认图表配置失败: {str(e)}"
        )

@router.put("/configs/{config_id}", response_model=ChartConfigResponse)
async def update_chart_config(
    config_id: str,
    config: ChartConfigCreate,
    current_user: dict = Depends(get_current_user_dependency)
):
    """更新图表配置"""
    supabase = get_supabase_client()
    
    try:
        # 验证配置权限
        config_result = supabase.table('chart_configs').select('*').eq('id', config_id).eq('user_id', current_user['id']).execute()
        if not config_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="图表配置不存在或无权限访问"
            )
        
        # 更新配置
        update_data = {
            "name": config.name,
            "config": config.config,
            "is_default": config.is_default
        }
        
        result = supabase.table('chart_configs').update(update_data).eq('id', config_id).execute()
        
        if result.data:
            config_data = result.data[0]
            return ChartConfigResponse(
                id=config_data['id'],
                name=config_data['name'],
                config=config_data['config'],
                is_default=config_data['is_default'],
                user_id=config_data['user_id'],
                created_at=config_data['created_at'],
                updated_at=config_data['updated_at']
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="更新图表配置失败"
            )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新图表配置失败: {str(e)}"
        )

@router.delete("/configs/{config_id}", response_model=MessageResponse)
async def delete_chart_config(
    config_id: str,
    current_user: dict = Depends(get_current_user_dependency)
):
    """删除图表配置"""
    supabase = get_supabase_client()
    
    try:
        # 验证配置权限
        config_result = supabase.table('chart_configs').select('*').eq('id', config_id).eq('user_id', current_user['id']).execute()
        if not config_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="图表配置不存在或无权限访问"
            )
        
        # 删除配置
        result = supabase.table('chart_configs').delete().eq('id', config_id).execute()
        
        return MessageResponse(message="图表配置删除成功")
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除图表配置失败: {str(e)}"
        )