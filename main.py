from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from datetime import date
import re

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

# 用户信息模型
class UserInfo(BaseModel):
    nickname: str
    email: EmailStr
    phone: str
    birthday: date
    gender: str

# 用户信息路由，用于新增或修改用户信息
@app.put("/user/info/")
async def update_user_info(user_info: UserInfo):
    """
    新增/修改用户信息
    :param user_info: 用户信息对象，包含昵称、邮箱、电话、生日和性别
    :return: 成功或失败消息
    """
    # 在此处添加逻辑，将用户信息存储到数据库中或进行相应的处理
    return {"message": "User information updated successfully"}

# 邮箱正则表达式
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# 电话号码正则表达式
PHONE_REGEX = r'^\d{3}-\d{3}-\d{4}$'

# 用户信息路由，用于获取用户信息
@app.get("/user/info/")
async def get_user_info():
    """
    获取用户信息
    :return: 用户信息对象
    """
    # 在此处添加逻辑，从数据库中获取用户信息或进行相应的处理
    # 这里仅作为示例返回固定的用户信息
    user_info = UserInfo(
        nickname="John Doe",
        email="johndoe@example.com",
        phone="123-456-7890",
        birthday=date(1990, 1, 1),
        gender="Male"
    )
    return user_info

# 将文档添加到 FastAPI 应用程序中
app.openapi_schema = None  # 让 FastAPI 自动生成文档

if __name__ == "__main__":
    import uvicorn

    # 启动 FastAPI 应用程序
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
