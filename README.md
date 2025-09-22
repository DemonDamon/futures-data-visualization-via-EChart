# 期货数据可视化平台

一个现代化的前后端分离期货数据可视化平台，支持实时数据展示、多种图表类型和响应式设计。

## 技术栈

### 前端
- React 18 + TypeScript
- Vite (构建工具)
- TailwindCSS (样式框架)
- ECharts (图表库)
- React Query (数据获取)
- React Router (路由)
- Heroicons (图标)

### 后端
- FastAPI (Python Web框架)
- MongoDB (数据库)
- Pandas (数据处理)
- Pydantic (数据验证)
- Uvicorn (ASGI服务器)

## 功能特性

- 📊 **多种图表类型**: 支持K线图、折线图等多种可视化方式
- 📁 **数据上传**: 支持CSV文件上传和数据导入
- 🔍 **合约选择**: 动态加载和选择期货合约
- 📱 **响应式设计**: 适配各种屏幕尺寸
- ⚡ **实时更新**: 支持数据实时刷新
- 🎨 **现代化UI**: 基于TailwindCSS的美观界面

## 项目结构

```
.
├── frontend/                 # 前端项目
│   ├── src/
│   │   ├── components/       # React组件
│   │   ├── pages/           # 页面组件
│   │   ├── services/        # API服务
│   │   └── main.tsx         # 入口文件
│   ├── package.json
│   └── vite.config.ts
├── backend/                  # 后端项目
│   ├── api/                 # API路由
│   ├── core/                # 核心配置
│   ├── models/              # 数据模型
│   ├── services/            # 业务逻辑
│   ├── main.py              # 入口文件
│   └── requirements.txt
└── README.md
```

## 快速开始

### 环境要求

- Node.js 18+
- Python 3.8+
- MongoDB 4.4+

### 安装依赖

#### 前端
```bash
cd frontend
npm install
```

#### 后端
```bash
cd backend
pip install -r requirements.txt
```

### 启动服务

#### 1. 启动MongoDB
```bash
# 确保MongoDB服务正在运行
mongod
```

#### 2. 启动后端服务
```bash
cd backend
python main.py
# 或使用uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. 启动前端服务
```bash
cd frontend
npm run dev
```

### 访问应用

- 前端: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 数据格式

### CSV文件格式要求

上传的CSV文件需要包含以下列：

| 列名 | 类型 | 描述 |
|------|------|------|
| instrument | string | 合约代码 |
| time | datetime | 时间 (YYYY-MM-DD HH:MM:SS) |
| interface | string | 接口类型 |
| open | float | 开盘价 |
| high | float | 最高价 |
| low | float | 最低价 |
| close | float | 收盘价 |
| volume | int | 成交量 |
| open_interest | int | 持仓量 (可选) |

### 示例数据

```csv
instrument,time,interface,open,high,low,close,volume,open_interest
RBHot,2023-01-01 09:00:00,5m,3500.0,3520.0,3495.0,3510.0,1000,5000
RBHot,2023-01-01 09:05:00,5m,3510.0,3530.0,3505.0,3525.0,1200,5100
```

## API接口

### 主要端点

- `GET /api/futures/data` - 获取期货数据
- `POST /api/futures/chart-data` - 获取图表数据
- `GET /api/futures/instruments` - 获取合约列表
- `POST /api/futures/upload` - 上传CSV文件
- `DELETE /api/futures/data` - 清空数据

详细API文档请访问: http://localhost:8000/docs

## 开发指南

### 前端开发

```bash
cd frontend
npm run dev      # 开发模式
npm run build    # 构建生产版本
npm run preview  # 预览生产版本
npm run lint     # 代码检查
```

### 后端开发

```bash
cd backend
python main.py                    # 启动开发服务器
uvicorn main:app --reload         # 使用uvicorn启动
```

## 部署

### 前端部署

```bash
cd frontend
npm run build
# 将dist目录部署到静态文件服务器
```

### 后端部署

```bash
cd backend
# 使用gunicorn部署
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 贡献

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。