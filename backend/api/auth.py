from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import timedelta
from models.schemas import UserCreate, UserLogin, UserResponse, Token, MessageResponse
from core.auth import get_password_hash, verify_password, create_access_token, verify_token
from core.database import get_supabase_client
from supabase import Client

router = APIRouter(prefix="/auth", tags=["认证"])
security = HTTPBearer()

@router.post("/register", response_model=MessageResponse)
async def register(user: UserCreate):
    """用户注册"""
    supabase = get_supabase_client()
    
    try:
        # 使用Supabase Auth注册用户
        auth_response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password
        })
        
        if auth_response.user:
            return MessageResponse(message="用户注册成功")
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="用户注册失败"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"注册过程中发生错误: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    """用户登录"""
    supabase = get_supabase_client()
    
    try:
        # 使用Supabase Auth登录
        auth_response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        
        if auth_response.user and auth_response.session:
            user_data = {
                "id": auth_response.user.id,
                "email": auth_response.user.email,
                "username": auth_response.user.email.split('@')[0],
                "created_at": auth_response.user.created_at
            }
            
            return Token(
                access_token=auth_response.session.access_token, 
                token_type="bearer",
                user=user_data
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="邮箱或密码错误"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"登录过程中发生错误: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """获取当前用户信息"""
    token = credentials.credentials
    payload = verify_token(token)
    
    supabase = get_supabase_client()
    
    try:
        result = supabase.table('users').select('*').eq('email', payload['sub']).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        user = result.data[0]
        return UserResponse(
            id=user['id'],
            username=user['username'],
            email=user['email'],
            created_at=user['created_at'],
            updated_at=user['updated_at']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取用户信息失败: {str(e)}"
        )

# 依赖项：获取当前用户
async def get_current_user_dependency(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """获取当前用户的依赖项"""
    token = credentials.credentials
    payload = verify_token(token)
    
    supabase = get_supabase_client()
    result = supabase.table('users').select('*').eq('email', payload['sub']).execute()
    
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    return result.data[0]