import psutil
import json
import time
import socket
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

# 创建 FastAPI 实例
app = FastAPI()

# 获取CPU使用率
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

# 获取内存使用率
def get_memory_usage():
    return psutil.virtual_memory().percent

# 获取磁盘使用率
def get_disk_usage():
    return psutil.disk_usage('/').percent

# 获取磁盘IO
def get_disk_io():
    return psutil.disk_io_counters()

# 获取进程数量
def get_process_count():
    return len(psutil.pids())

# 获取线程数量
def get_thread_count():
    return psutil.cpu_count()

# 获取沉睡进程数量
def get_sleeping_process_count():
    return len([p for p in psutil.process_iter() if p.status() == psutil.STATUS_SLEEPING])

# 获取最占CPU前10进程
def get_top_cpu_processes():
    try:
        processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']), key=lambda p: p.info['cpu_percent'] or 0, reverse=True)
        top_10_processes = [{'进程名': p.info['name'], 'CPU使用率': p.info['cpu_percent']} for p in processes[:10]]
        return top_10_processes
    except psutil.AccessDenied:
        print("无法访问进程信息，请确保脚本以管理员权限运行。")
        return []

# 获取最占内存前10进程
def get_top_memory_processes():
    try:
        processes = sorted(psutil.process_iter(['pid', 'name', 'memory_percent']), key=lambda p: p.info['memory_percent'] or 0, reverse=True)
        top_10_processes = [{'进程名': p.info['name'], '内存使用率': p.info['memory_percent']} for p in processes[:10]]
        return top_10_processes
    except psutil.AccessDenied:
        print("无法访问进程信息，请确保脚本以管理员权限运行。")
        return []

# 获取主机名
def get_hostname():
    return socket.gethostname()

# 获取内网IP地址
def get_intranet_ip():
    return socket.gethostbyname(socket.gethostname())

# 获取公网IP地址
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        public_ip = response.json()['ip']
        return public_ip
    except Exception as e:
        print("获取公网IP失败:", e)
        return "获取失败"

# 生成页面
@app.get("/html")
def generate_html():
    hostname = get_hostname()
    intranet_ip = get_intranet_ip()
    public_ip = get_public_ip()
    cpu_usage = get_cpu_usage()
    memory_usage = get_memory_usage()
    disk_usage = get_disk_usage()
    disk_io = get_disk_io()
    process_count = get_process_count()
    thread_count = get_thread_count()
    sleeping_process_count = get_sleeping_process_count()
    top_cpu_processes = get_top_cpu_processes()
    top_memory_processes = get_top_memory_processes()
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>System Resource Usage</title>
        <style>
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            tr:nth-child(even) {{
                background-color: #dddddd;
            }}
        </style>
    </head>
    <body>
        <h1>System Resource Usage</h1>
        <table>
            <tr>
                <th>主机名</th>
                <th>公网IP</th>
                <th>内网IP</th>
                <th>CPU使用率</th>
                <th>内存使用率</th>
                <th>磁盘使用率</th>
                <th>磁盘IO</th>
                <th>进程数量</th>
                <th>线程数量</th>
                <th>沉睡进程数量</th>
                <th>最占CPU前10进程</th>
                <th>最占内存前10进程</th>
            </tr>
            <tr>
                <td>{hostname}</td>
                <td>{public_ip}</td>
                <td>{intranet_ip}</td>
                <td>{cpu_usage}</td>
                <td>{memory_usage}</td>
                <td>{disk_usage}</td>
                <td>{disk_io}</td>
                <td>{process_count}</td>
                <td>{thread_count}</td>
                <td>{sleeping_process_count}</td>
                <td>{top_cpu_processes}</td>
                <td>{top_memory_processes}</td>
            </tr>
        </table>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

# 启动 FastAPI 应用程序
if __name__ == "__main__":
    import uvicorn
    from fastapi.responses import HTMLResponse

    uvicorn.run("agent:app", host="0.0.0.0", port=8001, reload=True)
