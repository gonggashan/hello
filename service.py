from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 创建 FastAPI 应用程序
app = FastAPI()

# 模拟数据库存储用户信息
fake_db = {}

# 定义用户模型
class User(BaseModel):
    username: str
    password: str

# 用户注册路由
@app.post("/register/")
async def register_user(user: User):
    """
    用户注册接口

    参数：
    - user: 包含用户名和密码的用户对象

    返回：
    - message: 注册成功消息
    - user_id: 用户ID
    - registration_time: 用户注册时间
    """
    # 检查用户名是否已经存在
    if user.username in fake_db:
        raise HTTPException(status_code=400, detail="Username already registered")

    # 模拟生成用户ID
    user_id = len(fake_db) + 1

    # 记录用户注册时间
    registration_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 将用户信息存储到数据库中
    fake_db[user.username] = {"user_id": user_id, "password": user.password, "registration_time": registration_time}

    return {"message": "User registered successfully", "user_id": user_id, "registration_time": registration_time}

# 将文档添加到 FastAPI 应用程序中
app.openapi_schema = None  # 让 FastAPI 自动生成文档

if __name__ == "__main__":
    import uvicorn

    # 启动 FastAPI 应用程序
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
