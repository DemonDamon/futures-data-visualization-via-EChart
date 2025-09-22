import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.database import test_connection
from api import auth, data, charts
from api.routes import futures

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api")
app.include_router(data.router, prefix="/api")
app.include_router(charts.router, prefix="/api")
app.include_router(futures.router, prefix="/api/futures")

@app.get("/")
async def root():
    return {"message": "期货数据可视化API服务正在运行"}

@app.get("/health")
async def health_check():
    """健康检查接口"""
    db_status = await test_connection()
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected",
        "message": "期货数据可视化API服务状态"
    }

@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    print(f"🚀 {settings.APP_NAME} 正在启动...")
    db_status = await test_connection()
    if db_status:
        print("✅ 数据库连接成功")
    else:
        print("❌ 数据库连接失败")

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    print(f"🛑 {settings.APP_NAME} 正在关闭...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)