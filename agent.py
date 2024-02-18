import psutil
import socket
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import time

# 创建 FastAPI 实例
app = FastAPI()

# 存储上一次的数值
prev_cpu_usage = 0.0
prev_memory_usage = 0.0
prev_disk_usage = 0.0
prev_disk_read = 0.0
prev_disk_write = 0.0
prev_process_count = 0
prev_thread_count = 0
prev_sleeping_process_count = 0
prev_processes = []

# 获取CPU使用率
def get_cpu_usage():
    global prev_cpu_usage
    cpu_usage = psutil.cpu_percent(interval=1)
    arrow = '🔺' if cpu_usage > prev_cpu_usage else '👇'
    color = 'red' if cpu_usage > prev_cpu_usage else 'green'
    prev_cpu_usage = cpu_usage
    return cpu_usage, arrow, color

# 获取内存使用率
def get_memory_usage():
    global prev_memory_usage
    mem = psutil.virtual_memory()
    memory_usage = mem.used / (1024 ** 3)
    arrow = '🔺' if memory_usage > prev_memory_usage else '👇'
    color = 'red' if memory_usage > prev_memory_usage else 'green'
    prev_memory_usage = memory_usage
    return memory_usage, arrow, color

# 获取磁盘使用率
def get_disk_usage():
    global prev_disk_usage
    disk = psutil.disk_usage('/')
    disk_usage = disk.used / (1024 ** 3)
    arrow = '🔺' if disk_usage > prev_disk_usage else '👇'
    color = 'red' if disk_usage > prev_disk_usage else 'green'
    prev_disk_usage = disk_usage
    return disk_usage, arrow, color

# 获取磁盘IO
def get_disk_io():
    global prev_disk_read, prev_disk_write
    io = psutil.disk_io_counters()
    disk_read = io.read_bytes / (1024 ** 2)
    disk_write = io.write_bytes / (1024 ** 2)
    read_arrow = '🔺' if disk_read > prev_disk_read else '👇'
    read_color = 'red' if disk_read > prev_disk_read else 'green'
    write_arrow = '🔺' if disk_write > prev_disk_write else '👇'
    write_color = 'red' if disk_write > prev_disk_write else 'green'
    prev_disk_read = disk_read
    prev_disk_write = disk_write
    return disk_read, read_arrow, read_color, disk_write, write_arrow, write_color

# 获取进程数量
def get_process_count():
    global prev_process_count
    process_count = len(psutil.pids())
    arrow = '🔺' if process_count > prev_process_count else '👇'
    color = 'red' if process_count > prev_process_count else 'green'
    prev_process_count = process_count
    return process_count, arrow, color

# 获取线程数量
def get_thread_count():
    global prev_thread_count
    thread_count = psutil.cpu_count()
    arrow = '🔺' if thread_count > prev_thread_count else '👇'
    color = 'red' if thread_count > prev_thread_count else 'green'
    prev_thread_count = thread_count
    return thread_count, arrow, color

# 获取沉睡进程数量
def get_sleeping_process_count():
    global prev_sleeping_process_count
    sleeping_process_count = len([p for p in psutil.process_iter() if p.status() == psutil.STATUS_SLEEPING])
    arrow = '🔺' if sleeping_process_count > prev_sleeping_process_count else '👇'
    color = 'red' if sleeping_process_count > prev_sleeping_process_count else 'green'
    prev_sleeping_process_count = sleeping_process_count
    return sleeping_process_count, arrow, color

# 获取主机名
def get_hostname():
    return socket.gethostname()

# 获取所有内网IP地址
def get_intranet_ips():
    ips = []
    interfaces = psutil.net_if_addrs()
    for interface_name, interface_addresses in interfaces.items():
        for address in interface_addresses:
            if address.family == socket.AF_INET:
                ips.append(address.address)
    return ips

# 获取公网IP地址
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        public_ip = response.json()['ip']
        return public_ip
    except Exception as e:
        print("获取公网IP失败:", e)
        return "获取失败"

# 获取系统全部进程信息
def get_all_processes():
    global prev_processes
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'create_time']):
        try:
            cpu_percent = proc.cpu_percent()
            memory_percent = proc.memory_percent()
            process_info = {
                'pid': proc.pid,
                'name': proc.info['name'] if 'name' in proc.info else '',
                'cpu_percent': cpu_percent if cpu_percent is not None else 0.0,
                'memory_percent': memory_percent if memory_percent is not None else 0.0,
                'create_time': time.time() - proc.create_time() if proc.create_time() is not None else 0
            }
            processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    arrow_processes = []
    for process in processes:
        prev_process = next((p for p in prev_processes if p['pid'] == process['pid']), None)
        if prev_process:
            process['cpu_arrow'] = '🔺' if process['cpu_percent'] > prev_process['cpu_percent'] else '👇'
            process['cpu_color'] = 'red' if process['cpu_percent'] > prev_process['cpu_percent'] else 'green'
            process['memory_arrow'] = '🔺' if process['memory_percent'] > prev_process['memory_percent'] else '👇'
            process['memory_color'] = 'red' if process['memory_percent'] > prev_process['memory_percent'] else 'green'
        else:
            process['cpu_arrow'] = ''
            process['cpu_color'] = ''
            process['memory_arrow'] = ''
            process['memory_color'] = ''
        arrow_processes.append(process)
    prev_processes = processes
    return arrow_processes

# 生成页面
@app.get("/html")
def generate_html():
    hostname = get_hostname()
    intranet_ips = get_intranet_ips()
    public_ip = get_public_ip()
    cpu_usage, cpu_arrow, cpu_color = get_cpu_usage()
    memory_usage, memory_arrow, memory_color = get_memory_usage()
    disk_usage, disk_arrow, disk_color = get_disk_usage()
    disk_read, read_arrow, read_color, disk_write, write_arrow, write_color = get_disk_io()
    process_count, process_arrow, process_color = get_process_count()
    thread_count, thread_arrow, thread_color = get_thread_count()
    sleeping_process_count, sleeping_arrow, sleeping_color = get_sleeping_process_count()
    all_processes = get_all_processes()

    style_css = """
        body {
            font-family: 'Courier New', Courier, monospace;
            padding: 20px;
            margin: 0;
            background-color: #000;
            color: #0f0;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 20px;
        }
        th, td {
            border: 1px solid #0f0;
            padding: 8px;
        }
        th {
            background-color: #00FF00;
            color: #000;
        }
        tr:nth-child(even) {
            background-color: #333;
        }
        .dataCell {
            font-weight: bold;
            color: #0f0;
        }
        .red {
            color: red;
        }
        .green {
            color: green;
        }
    """

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>系统监控</title>
        <style>
            {style_css}
        </style>
    </head>
    <body>
        <h4>系统监控</h4>
        <table>
            <tr>
                <th>主机名</th>
                <th>公网IP</th>
                <th>内网IP</th>
            </tr>
            <tr>
                <td>{hostname}</td>
                <td>{public_ip}</td>
                <td>{'<br>'.join(intranet_ips)}</td>
            </tr>
        </table>
        <table>
            <tr>
                <th>数据</th>
                <th>值</th>
                <th>变化</th>
            </tr>
            <tr>
                <td>CPU使用率</td>
                <td class="dataCell {cpu_color}">{cpu_usage}%</td>
                <td class="{cpu_color}">{cpu_arrow}</td>
            </tr>
            <tr>
                <td>内存使用率</td>
                <td class="dataCell {memory_color}">{memory_usage:.2f}GB</td>
                <td class="{memory_color}">{memory_arrow}</td>
            </tr>
            <tr>
                <td>磁盘使用率</td>
                <td class="dataCell {disk_color}">{disk_usage:.2f}GB</td>
                <td class="{disk_color}">{disk_arrow}</td>
            </tr>
            <tr>
                <td>磁盘IO (读取/写入)</td>
                <td class="dataCell {read_color}">{disk_read:.2f}MB / {disk_write:.2f}MB</td>
                <td class="{read_color}">{read_arrow} / {write_arrow}</td>
            </tr>
            <tr>
                <td>进程数量</td>
                <td class="dataCell {process_color}">{process_count}</td>
                <td class="{process_color}">{process_arrow}</td>
            </tr>
            <tr>
                <td>线程数量</td>
                <td class="dataCell {thread_color}">{thread_count}</td>
                <td class="{thread_color}">{thread_arrow}</td>
            </tr>
            <tr>
                <td>沉睡进程数量</td>
                <td class="dataCell {sleeping_color}">{sleeping_process_count}</td>
                <td class="{sleeping_color}">{sleeping_arrow}</td>
            </tr>
        </table>
        <h4>系统全部进程信息</h4>
        <table>
            <tr>
                <th>PID</th>
                <th>名称</th>
                <th>CPU%</th>
                <th>内存%</th>
                <th>变化</th>
            </tr>
    """

    for process in all_processes:
        html_content += f"""
            <tr>
                <td>{process['pid']}</td>
                <td>{process['name']}</td>
                <td class="{process['cpu_color']}">{process['cpu_percent']}</td>
                <td class="{process['memory_color']}">{process['memory_percent']}</td>
                <td class="{process['cpu_color']}">{process['cpu_arrow']}</td>
            </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content, status_code=200)

# 启动 FastAPI 应用程序
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("agent:app", host="0.0.0.0", port=8001, reload=True)
