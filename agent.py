import psutil
import socket
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import time
from threading import Thread

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

# 自动刷新间隔（默认3秒）
auto_refresh_interval = 3

# 获取CPU使用率
def get_cpu_usage():
    global prev_cpu_usage
    cpu_usage = psutil.cpu_percent(interval=1)
    arrow = '🔺' if cpu_usage > prev_cpu_usage else '👇'
    color = 'red' if cpu_usage > prev_cpu_usage else 'green'
    prev_cpu_usage = cpu_usage
    return f"{cpu_usage}% {arrow}", color

# 获取内存使用率
def get_memory_usage():
    global prev_memory_usage
    mem = psutil.virtual_memory()
    memory_usage = mem.used / (1024 ** 3)
    arrow = '🔺' if memory_usage > prev_memory_usage else '👇'
    color = 'red' if memory_usage > prev_memory_usage else 'green'
    prev_memory_usage = memory_usage
    return f"{memory_usage:.2f}GB {arrow}", color

# 获取磁盘使用率
def get_disk_usage():
    global prev_disk_usage
    disk = psutil.disk_usage('/')
    disk_usage = disk.used / (1024 ** 3)
    arrow = '🔺' if disk_usage > prev_disk_usage else '👇'
    color = 'red' if disk_usage > prev_disk_usage else 'green'
    prev_disk_usage = disk_usage
    return f"{disk_usage:.2f}GB {arrow}", color

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
    return f"{disk_read:.2f}MB {read_arrow}", read_color, f"{disk_write:.2f}MB {write_arrow}", write_color

# 获取进程数量
def get_process_count():
    global prev_process_count
    process_count = len(psutil.pids())
    arrow = '🔺' if process_count > prev_process_count else '👇'
    color = 'red' if process_count > prev_process_count else 'green'
    prev_process_count = process_count
    return f"{process_count} {arrow}", color

# 获取线程数量
def get_thread_count():
    global prev_thread_count
    thread_count = psutil.cpu_count()
    arrow = '🔺' if thread_count > prev_thread_count else '👇'
    color = 'red' if thread_count > prev_thread_count else 'green'
    prev_thread_count = thread_count
    return f"{thread_count} {arrow}", color

# 获取沉睡进程数量
def get_sleeping_process_count():
    global prev_sleeping_process_count
    sleeping_process_count = len([p for p in psutil.process_iter() if p.status() == psutil.STATUS_SLEEPING])
    arrow = '🔺' if sleeping_process_count > prev_sleeping_process_count else '👇'
    color = 'red' if sleeping_process_count > prev_sleeping_process_count else 'green'
    prev_sleeping_process_count = sleeping_process_count
    return f"{sleeping_process_count} {arrow}", color

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
def get_all_processes(sort_key=None, reverse=False):
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

    # 检查指定的排序键是否存在于进程信息中
    if sort_key and sort_key in processes[0]:
        processes.sort(key=lambda x: x[sort_key], reverse=reverse)
    else:
        # 如果指定的键不存在，则默认使用 'cpu_percent' 进行排序
        processes.sort(key=lambda x: x['cpu_percent'], reverse=reverse)

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
def generate_html(sort_key: str = None, reverse: bool = False, refresh_interval: int = 3):
    global auto_refresh_interval
    auto_refresh_interval = refresh_interval
    hostname = get_hostname()
    intranet_ips = get_intranet_ips()
    public_ip = get_public_ip()
    cpu_usage, cpu_color = get_cpu_usage()
    memory_usage, memory_color = get_memory_usage()
    disk_usage, disk_color = get_disk_usage()
    disk_read, read_color, disk_write, write_color = get_disk_io()
    process_count, process_color = get_process_count()
    thread_count, thread_color = get_thread_count()
    sleeping_process_count, sleeping_color = get_sleeping_process_count()
    all_processes = get_all_processes(sort_key, reverse)

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
        .refresh {
            position: absolute;
            top: 20px;
            left: 20px;
            display: flex;
            align-items: center;
            color: green;
        }
        .refresh input[type='number'], .refresh button {
            background-color: #333;
            color: #0f0;
            border: 1px solid #0f0;
            padding: 5px;
            border-radius: 3px;
            margin-right: 5px;
        }
        .refresh label {
            margin-right: 10px;
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
        <div class="refresh">
            <form action="/html" method="get">
                <label for="refresh_interval">系统监控自动刷新间隔（秒）：</label>
                <input type="number" id="refresh_interval" name="refresh_interval" min="1" value="{auto_refresh_interval}">
                <button type="submit">更新</button>
            </form>
        </div>
        <h4></h4>
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
            </tr>
            <tr>
                <td>CPU使用率: <span class="{cpu_color}">{cpu_usage}</span></td>
            </tr>
            <tr>
                <td>内存使用率: <span class="{memory_color}">{memory_usage}</span></td>
            </tr>
            <tr>
                <td>磁盘使用率: <span class="{disk_color}">{disk_usage}</span></td>
            </tr>
            <tr>
                <td>磁盘IO (读取): <span class="{read_color}">{disk_read}</span></td>
            </tr>
            <tr>
                <td>磁盘IO (写入): <span class="{write_color}">{disk_write}</span></td>
            </tr>
            <tr>
                <td>进程数量: <span class="{process_color}">{process_count}</span></td>
            </tr>
            <tr>
                <td>线程数量: <span class="{thread_color}">{thread_count}</span></td>
            </tr>
            <tr>
                <td>沉睡进程数量: <span class="{sleeping_color}">{sleeping_process_count}</span></td>
            </tr>
        </table>
        <h4>系统全部进程信息</h4>
        <table>
            <tr>
                <th>PID</th>
                <th>名称</th>
                <th>
                    CPU% 
                    <a href="?sort_key=cpu_percent&reverse=False">&#9660;</a>
                    <a href="?sort_key=cpu_percent&reverse=True">&#9650;</a>
                </th>
                <th>
                    内存% 
                    <a href="?sort_key=memory_percent&reverse=False">&#9660;</a>
                    <a href="?sort_key=memory_percent&reverse=True">&#9650;</a>
                </th>
            </tr>
    """

    for process in all_processes:
        html_content += f"""
            <tr>
                <td>{process['pid']}</td>
                <td>{process['name']}</td>
                <td class="{process['cpu_color']}">{process['cpu_percent']} {process['cpu_arrow']}</td>
                <td class="{process['memory_color']}">{process['memory_percent']} {process['memory_arrow']}</td>
            </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content, status_code=200)

# 自动刷新页面数据的线程函数
def auto_refresh_data():
    global auto_refresh_interval
    while True:
        time.sleep(auto_refresh_interval)
        requests.get("http://localhost:8001/html")

# 启动自动刷新页面数据的线程
refresh_thread = Thread(target=auto_refresh_data)
refresh_thread.daemon = True
refresh_thread.start()

# 启动 FastAPI 应用程序
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("agent:app", host="0.0.0.0", port=8001, reload=True)
