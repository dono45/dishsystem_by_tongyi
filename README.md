"# 餐饮点餐系统

一个基于Vue.js和Flask的现代化餐饮点餐平台，支持用户注册登录、浏览菜品、购物车管理、下单、评论等功能。

## 项目概述

本项目是一个完整的餐饮点餐系统，包含前端和后端两部分。用户可以浏览菜品、添加到购物车、下单购买，还可以对菜品进行评价。管理员可以管理菜品和订单。

## 技术栈

### 前端
- Vue.js 3
- Vue Router
- Bootstrap 5
- Axios

### 后端
- Flask (Python)
- Flask-SQLAlchemy (ORM)
- Flask-JWT-Extended (身份验证)
- SQLite (数据库)

## 功能特性

### 用户功能
- 用户注册和登录
- 浏览菜品列表
- 搜索和筛选菜品
- 查看菜品详情
- 添加菜品到购物车（可选择规格）
- 管理购物车
- 创建订单
- 查看订单历史
- 对菜品进行评价

### 管理员功能
- 管理菜品（增删改查）
- 管理订单（查看、更新状态）

## 项目结构

```
.
├── backend/          # 后端代码
│   ├── app.py        # 主应用文件
│   ├── models.py     # 数据模型
│   └── requirements.txt # Python依赖
└── frontend/         # 前端代码
    ├── src/
    │   ├── components/ # Vue组件
    │   ├── App.vue     # 主应用组件
    │   └── main.js     # 应用入口
    └── package.json    # Node.js依赖
```

## 安装和运行

### 后端

1. 进入后端目录：
   ```
   cd backend
   ```

2. 创建虚拟环境（推荐）：
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate  # Windows
   ```

3. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

4. 运行应用：
   ```
   python app.py
   ```

   后端服务将运行在 `http://localhost:5000`

### 前端

1. 进入前端目录：
   ```
   cd frontend
   ```

2. 安装依赖：
   ```
   npm install
   ```

3. 运行开发服务器：
   ```
   npm run serve
   ```

   前端开发服务器将运行在 `http://localhost:8080`

## 默认账户

- 管理员账户：
  - 用户名：`admin`
  - 密码：`admin123`

## API接口

主要的API接口包括：

- 用户认证：`/api/register`, `/api/login`
- 菜品管理：`/api/dishes`
- 购物车：`/api/cart`
- 订单：`/api/orders`
- 评论：`/api/dishes/<id>/reviews`
- 管理员接口：`/api/admin/*`

详细接口文档请查看后端代码中的路由定义。

## 开发

### 前端开发

前端使用Vue.js框架，组件位于`frontend/src/components/`目录下。

### 后端开发

后端使用Flask框架，主要功能在`app.py`中实现，数据模型定义在`models.py`中。

## 部署

在生产环境中，建议使用Nginx作为反向代理，使用Gunicorn运行Flask应用。

## 许可证

本项目仅供学习和参考使用。" 
