from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

# 创建 FastAPI 应用程序
app = FastAPI()

# 模拟数据库存储用户信息
fake_db = {}
fake_recharge_db = {}  # 模拟存储用户充值信息
fake_consumption_db = {}  # 模拟存储用户消费信息

# 定义用户模型
class User(BaseModel):
    username: str
    password: str

# 模拟在线用户的列表
online_users = []

# 用户充值记录
class RechargeRecord:
    def __init__(self, user_id: str, amount: float, timestamp: str):
        self.user_id = user_id
        self.amount = amount
        self.timestamp = timestamp

recharge_records = []

# 用户消费套餐记录
class PackageConsumption:
    def __init__(self, user_id: str, package_type: str, amount: float, timestamp: str):
        self.user_id = user_id
        self.package_type = package_type
        self.amount = amount
        self.timestamp = timestamp

package_consumptions = []

# 用户信息
class UserInfo:
    def __init__(self, user_id: str, username: str, password: str, email: str, phone: str):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone

user_info = {}

# 用户信息模型
class UserInfo(BaseModel):
    nickname: str
    email: EmailStr
    phone: str
    birthday: date
    gender: str

#用户套餐测试数据
user_packages = {
    "VIP_level": "VIP3",
    "recharge_minutes": 1000,
    "daily_package_minutes": 120,
    "weekly_package_minutes": 300,
    "monthly_package_minutes": 600,
    "event_gift_minutes": 50,
    "night_package_minutes": 200,
    "last_usage_time": datetime.now(),  # 上次消费时间
}

# 枚举用户充值方式
class RechargeMethod(str, Enum):
    CASH = "现金"
    ALIPAY = "支付宝"
    WECHAT = "微信"
    GCASH = "Gcash"
    USDT = "USDT"

# 用户充值请求模型
class RechargeRequest(BaseModel):
    user_id: int
    amount: float
    method: RechargeMethod
    user_package: str

# 邮箱正则表达式
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# 电话号码正则表达式
PHONE_REGEX = r'^\d{3}-\d{3}-\d{4}$'

# 用户注册路由
@app.post("/register/", tags=["用户注册"])
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
        raise HTTPException(status_code=400, detail="用户名已被注册")

    # 模拟生成用户ID
    user_id = len(fake_db) + 1

    # 记录用户注册时间
    registration_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 将用户信息存储到数据库中
    fake_db[user.username] = {"user_id": user_id, "password": user.password, "registration_time": registration_time}

    return {"message": "用户注册成功", "user_id": user_id, "registration_time": registration_time}

# 用户信息路由，用于新增或修改用户信息
@app.put("/user/change_info/", tags=["新增或修改用户信息"])
async def update_user_info(user_info: UserInfo):
    """
    新增/修改用户信息

    参数：
    - user_info: 用户信息对象，包含昵称、邮箱、电话、生日和性别

    返回：
    - message: 成功或失败消息
    """
    # 在此处添加逻辑，将用户信息存储到数据库中或进行相应的处理
    return {"message": "用户信息更新成功"}

# 用户信息路由，用于获取用户信息
@app.get("/user/get_info/", tags=["获取用户信息"])
async def get_user_info():
    """
    获取用户信息

    返回：
    - 用户信息对象
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

# 用户充值路由
@app.post("/recharge/", tags=["用户充值"])
async def recharge_user(recharge_request: RechargeRequest):
    """
    用户充值接口

    参数：
    - recharge_request: 包含用户ID、充值金额和充值方式的请求对象

    返回：
    - message: 充值成功消息
    """
    # 在此处添加逻辑，处理用户充值请求，更新用户的充值信息和会员等级

    # 将充值信息存储到数据库中（此处仅作示例，实际应用需要持久化存储）
    recharge_info = {
        "user_id": recharge_request.user_id,
        "amount": recharge_request.amount,
        "method": recharge_request.method.value,  # 将枚举类型转换为字符串
        "user_package": recharge_request.user_package,
        "recharge_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    fake_recharge_db[len(fake_recharge_db) + 1] = recharge_info

    # 更新用户套餐信息
    # 此处需要添加逻辑，根据不同的充值方式进行相应的套餐增加

    # 返回充值成功消息
    return {"message": "用户充值成功"}

# 用户中心路由，用于展示用户套餐信息
@app.get("/user/packages/", tags=["展示用户套餐信息"])
async def get_user_packages():
    """
    获取用户套餐信息

    返回：
    - 用户套餐信息
    """
    return user_packages

# 统计在线用户接口
@app.get("/online_users", response_model=List[str], tags=["统计在线用户"])
async def get_online_users():
    """
    获取当前在线用户列表
    """
    return online_users

# 用户充值统计接口
@app.get("/recharge_statistics", tags=["统计用户充值"])
async def get_recharge_statistics(
    start_date: Optional[str] = Query(None, description="开始日期，格式为YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期，格式为YYYY-MM-DD"),
):
    """
    统计用户充值情况，可以按日、周、月等时间段统计
    """
    # 这里可以根据 start_date 和 end_date 进行相应的统计逻辑
    return {"message": "根据时间段统计用户充值情况"}

# 用户套餐消费统计接口
@app.get("/package_consumption_statistics", tags=["统计用户各种套餐消费情况"])
async def get_package_consumption_statistics(
    start_date: Optional[str] = Query(None, description="开始日期，格式为YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期，格式为YYYY-MM-DD"),
):
    """
    统计用户套餐消费情况，可以按日、周、月等时间段统计
    """
    # 这里可以根据 start_date 和 end_date 进行相应的统计逻辑
    return {"message": "根据时间段统计用户套餐消费情况"}

# 修改用户账号密码接口
@app.put("/user/{user_id}/password", tags=["修改用户账号密码"])
async def update_user_password(
    user_id: str,
    password: str
):
    """
    修改用户账号密码
    """
    # 在这里实现修改用户密码的逻辑
    return {"message": f"用户 {user_id} 密码已修改"}

# 修改用户个人信息接口
@app.put("/user/{user_id}/info", tags=["修改用户个人信息"])
async def update_user_info(
    user_id: str,
    username: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
):
    """
    修改用户个人信息，包括用户名、邮箱、电话号码等
    """
    # 在这里实现修改用户个人信息的逻辑
    return {"message": f"用户 {user_id} 个人信息已更新"}

# 黑名单列表禁用用户接口
@app.put("/user/{user_id}/blacklist", tags=["黑名单列表禁用用户"])
async def add_to_blacklist(
    user_id: str
):
    """
    将用户加入黑名单，禁止用户访问网吧
    """
    # 在这里实现将用户加入黑名单的逻辑
    return {"message": f"用户 {user_id} 已加入黑名单"}

# 启动 FastAPI 应用程序
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

