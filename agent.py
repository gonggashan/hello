import psutil
import socket
import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import asyncio

app = FastAPI()
static_system_info = {}  # 全局变量存储静态系统信息
previous_dynamic_system_info = {}  # 全局变量存储上次动态系统信息


def get_static_system_info():  # 获取静态系统信息
    global static_system_info
    if not static_system_info:
        static_system_info['hostname'] = socket.gethostname()
        static_system_info['intranet_ips'] = '  '.join(
            [address.address for interface_addresses in psutil.net_if_addrs().values()
             for address in interface_addresses if address.family == socket.AF_INET])
        static_system_info['public_ip'] = requests.get('https://api.ipify.org?format=json').json().get('ip',
                                                                                                         '获取失败')
        static_system_info['cpu_cores'] = f"{psutil.cpu_count(logical=False)} 核心"
        mem = psutil.virtual_memory()
        static_system_info['memory_size'] = f"{mem.total / (1024 ** 3):.2f} GB"  # Convert bytes to GB


def get_dynamic_system_info():  # 获取动态系统信息
    cpu_usage = f"{psutil.cpu_percent()} %"  # CPU usage percentage
    disk = psutil.disk_usage('/')
    disk_usage = f"{disk.used / (1024 ** 3):.2f} %"  # Convert bytes to GB
    process_count = len(psutil.pids())
    thread_count = psutil.cpu_count()
    sleeping_process_count = len([p for p in psutil.process_iter() if p.status() == psutil.STATUS_SLEEPING])
    io = psutil.disk_io_counters()
    disk_read = f"{io.read_bytes / (1024 ** 2):.2f} MB/s"  # Convert bytes to MB
    disk_write = f"{io.write_bytes / (1024 ** 2):.2f} MB/s"  # Convert bytes to MB
    network = psutil.net_io_counters()
    sent = f"{network.bytes_sent / (1024 ** 2):.2f} MB/s"  # Convert bytes to MB
    received = f"{network.bytes_recv / (1024 ** 2):.2f} MB/s"  # Convert bytes to MB
    return {
        'cpu_usage': cpu_usage,
        'disk_usage': disk_usage,
        'process_count': process_count,
        'thread_count': thread_count,
        'sleeping_process_count': sleeping_process_count,
        'disk_read': disk_read,
        'disk_write': disk_write,
        'sent_speed': sent,
        'received_speed': received
    }


@app.get("/")
async def generate_html():
    global previous_dynamic_system_info
    get_static_system_info()  # 获取静态系统信息
    dynamic_system_info = get_dynamic_system_info()  # 获取动态系统信息
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>系统监控</title>
        <style>
            body {{
                background-color: #282828;
                color: #00ff00;
                font-family: Arial, sans-serif;
                padding: 20px;
                max-width: 800px;
                margin: auto;
            }}
            pre {{
                background-color: #282828;
                padding: 20px;
                border-radius: 10px;
                white-space: pre-wrap;
                word-wrap: break-word;
            }}
            .yellow {{
                color: yellow;
            }}
        </style>
        <meta http-equiv="refresh" content="3">
    </head>
    <body>
        <pre>
            pod            == {static_system_info['hostname']} 
            公网IP         == {static_system_info['public_ip']} 
            内网IP         == {static_system_info['intranet_ips']} 
            CPU核心数      == {static_system_info['cpu_cores']}
            CPU使用率      == <span class="{ 'yellow' if dynamic_system_info['cpu_usage'] > previous_dynamic_system_info.get('cpu_usage', '0 %') else '' }">{dynamic_system_info['cpu_usage']}</span>
            内存大小       == {static_system_info['memory_size']} 
            磁盘使用率     == <span class="{ 'yellow' if dynamic_system_info['disk_usage'] > previous_dynamic_system_info.get('disk_usage', '0 %') else '' }">{dynamic_system_info['disk_usage']}</span>
            进程数量       == {dynamic_system_info['process_count']} 
            线程数量       == {dynamic_system_info['thread_count']} 
            沉睡进程数量   == {dynamic_system_info['sleeping_process_count']} 
            磁盘IO (读)    == <span class="{ 'yellow' if dynamic_system_info['disk_read'] > previous_dynamic_system_info.get('disk_read', '0 MB/s') else '' }">{dynamic_system_info['disk_read']}</span>
            磁盘IO (写)    == <span class="{ 'yellow' if dynamic_system_info['disk_write'] > previous_dynamic_system_info.get('disk_write', '0 MB/s') else '' }">{dynamic_system_info['disk_write']}</span>
            网络发送速度   == <span class="{ 'yellow' if dynamic_system_info['sent_speed'] > previous_dynamic_system_info.get('sent_speed', '0 MB/s') else '' }">{dynamic_system_info['sent_speed']}</span>
            网络接收速度   == <span class="{ 'yellow' if dynamic_system_info['received_speed'] > previous_dynamic_system_info.get('received_speed', '0 MB/s') else '' }">{dynamic_system_info['received_speed']}</span>
        </pre>
    </body>
    </html>
    """
    previous_dynamic_system_info = dynamic_system_info  # 更新上次动态系统信息
    return HTMLResponse(content=html_content, status_code=200)


if __name__ == "__main__":
    uvicorn.run("agent:app", host="0.0.0.0", port=8001, reload=True)
