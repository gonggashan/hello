import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class HostInfo(BaseModel):
    ip: str
    hostname: str

@app.post("/register_host/")
async def register_host(host_info: HostInfo):
    ip = host_info.ip
    hostname = host_info.hostname
    # 在这里执行你的逻辑，比如保存到数据库或者做其他处理
    return {"message": f"Received host information - IP: {ip}, Hostname: {hostname}"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
