from supabase import create_client, Client
from .config import settings

# 创建Supabase客户端
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)

# 获取Supabase客户端实例
def get_supabase_client() -> Client:
    return supabase

# 数据库连接测试
async def test_connection():
    try:
        # 测试连接
        result = supabase.table('users').select('*').limit(1).execute()
        return True
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return False