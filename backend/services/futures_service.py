import pandas as pd
from typing import Optional, List, Dict, Any
from datetime import datetime
from fastapi import UploadFile
from core.database import get_supabase_client
from models.futures import (
    FuturesData,
    FuturesDataResponse,
    ChartDataRequest,
    ChartDataResponse,
    UploadResponse
)
import io

class FuturesService:
    def __init__(self):
        self.supabase = get_supabase_client()
    
    async def get_futures_data(
        self,
        instrument: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        page: int = 1,
        page_size: int = 100
    ) -> FuturesDataResponse:
        """获取期货数据"""
        try:
            # 构建查询
            query = self.supabase.table('kline_data').select('*')
            
            if start_time:
                query = query.gte('datetime', start_time.isoformat())
            if end_time:
                query = query.lte('datetime', end_time.isoformat())
            
            # 获取总数
            count_result = query.execute()
            total = len(count_result.data) if count_result.data else 0
            
            # 分页查询
            start = (page - 1) * page_size
            end = start + page_size - 1
            
            result = query.order('datetime').range(start, end).execute()
            
            if not result.data:
                return FuturesDataResponse(
                    data=[],
                    total=0,
                    page=page,
                    page_size=page_size
                )
            
            data = []
            for row in result.data:
                data.append(FuturesData(
                    instrument=row.get('dataset_id', 'unknown'),
                    time=datetime.fromisoformat(row['datetime'].replace('Z', '+00:00')),
                    interface=row.get('timeframe', 'default'),
                    open=float(row['open_price']),
                    high=float(row['high_price']),
                    low=float(row['low_price']),
                    close=float(row['close_price']),
                    volume=int(row['volume']),
                    open_interest=None
                ))
            
            return FuturesDataResponse(
                data=data,
                total=total,
                page=page,
                page_size=page_size
            )
        except Exception as e:
            raise Exception(f"获取期货数据失败: {str(e)}")
    
    async def get_chart_data(self, request: ChartDataRequest) -> ChartDataResponse:
        """获取图表数据"""
        try:
            query = self.supabase.table('kline_data').select('*')
            
            if request.start_time:
                query = query.gte('datetime', request.start_time.isoformat())
            if request.end_time:
                query = query.lte('datetime', request.end_time.isoformat())
            
            result = query.order('datetime').execute()
            
            data = []
            for row in result.data:
                timestamp = int(datetime.fromisoformat(row['datetime'].replace('Z', '+00:00')).timestamp() * 1000)
                data.append([
                    timestamp,
                    float(row['open_price']),
                    float(row['close_price']),
                    float(row['low_price']),
                    float(row['high_price']),
                    int(row['volume'])
                ])
            
            return ChartDataResponse(
                instrument=request.instrument,
                data=data
            )
        except Exception as e:
            raise Exception(f"获取图表数据失败: {str(e)}")
    
    async def get_instruments(self) -> List[str]:
        """获取所有合约代码"""
        try:
            # 查询所有不重复的timeframe作为合约类型
            result = self.supabase.table('kline_data').select('timeframe').execute()
            
            if not result.data:
                return []
            
            # 去重并返回
            instruments = list(set(item['timeframe'] for item in result.data if item.get('timeframe')))
            return sorted(instruments)
        except Exception as e:
            raise Exception(f"获取合约代码失败: {str(e)}")
    
    async def upload_csv_file(self, file: UploadFile) -> UploadResponse:
        """上传CSV文件"""
        try:
            # 读取CSV文件
            content = await file.read()
            df = pd.read_csv(io.StringIO(content.decode('utf-8')))
            
            # 数据预处理和列名映射
            df['time'] = pd.to_datetime(df['time'], format='%Y%m%d%H%M%S').dt.strftime('%Y-%m-%dT%H:%M:%S')
            
            # 映射CSV列名到数据库列名
            column_mapping = {
                'time': 'datetime',
                'open': 'open_price',
                'high': 'high_price', 
                'low': 'low_price',
                'close': 'close_price',
                'volume': 'volume'
            }
            
            # 选择需要的列并重命名
            df_mapped = df[list(column_mapping.keys())].rename(columns=column_mapping)
            
            # 添加默认的dataset_id和timeframe
            df_mapped['dataset_id'] = '550e8400-e29b-41d4-a716-446655440001'
            df_mapped['timeframe'] = '5m'  # 根据文件名RBHot_5m.csv判断为5分钟数据
            
            # 转换为字典列表
            data_list = df_mapped.to_dict('records')
            
            # 批量插入数据库
            if data_list:
                # Supabase批量插入
                result = self.supabase.table('kline_data').insert(data_list).execute()
                if not result.data:
                    raise Exception("数据插入失败")
            
            return UploadResponse(
                message="文件上传成功",
                filename=file.filename,
                records_count=len(data_list)
            )
        except Exception as e:
            raise Exception(f"文件上传失败: {str(e)}")
    
    async def clear_data(self, instrument: Optional[str] = None) -> Dict[str, Any]:
        """清空数据"""
        try:
            if instrument:
                # 删除指定timeframe的数据
                result = self.supabase.table('kline_data').delete().eq('timeframe', instrument).execute()
            else:
                # 删除所有数据
                result = self.supabase.table('kline_data').delete().neq('id', '').execute()
            
            # 返回删除的记录数
            return len(result.data) if result.data else 0
        except Exception as e:
            raise Exception(f"清空数据失败: {str(e)}")