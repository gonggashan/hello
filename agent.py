import psutil
import json
import time
from fastapi import FastAPI, HTTPException

# 创建 FastAPI 实例
app = FastAPI()

# 获取CPU使用率
def get_cpu_usage():
    return {"CPU使用率": psutil.cpu_percent(interval=1)}

# 获取内存使用率
def get_memory_usage():
    return {"内存使用率": psutil.virtual_memory().percent}

# 获取磁盘使用率
def get_disk_usage():
    return {"磁盘使用率": psutil.disk_usage('/').percent}

# 获取磁盘IO
def get_disk_io():
    return {"磁盘IO": psutil.disk_io_counters()}

# 获取进程数量
def get_process_count():
    return {"进程数量": len(psutil.pids())}

# 获取线程数量
def get_thread_count():
    return {"线程数量": psutil.cpu_count()}

# 获取沉睡进程数量
def get_sleeping_process_count():
    return {"沉睡进程数量": len([p for p in psutil.process_iter() if p.status() == psutil.STATUS_SLEEPING])}

# 获取最占CPU前10进程
def get_top_cpu_processes():
    try:
        processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']), key=lambda p: p.info['cpu_percent'] or 0, reverse=True)
        top_10_processes = [{'进程名': p.info['name'], 'CPU使用率': p.info['cpu_percent']} for p in processes[:10]]
        return {"最占CPU前10进程": top_10_processes}
    except psutil.AccessDenied:
        print("无法访问进程信息，请确保脚本以管理员权限运行。")
        return []

# 获取最占内存前10进程
def get_top_memory_processes():
    try:
        processes = sorted(psutil.process_iter(['pid', 'name', 'memory_percent']), key=lambda p: p.info['memory_percent'] or 0, reverse=True)
        top_10_processes = [{'进程名': p.info['name'], '内存使用率': p.info['memory_percent']} for p in processes[:10]]
        return {"最占内存前10进程": top_10_processes}
    except psutil.AccessDenied:
        print("无法访问进程信息，请确保脚本以管理员权限运行。")
        return []

# 路由，实时返回系统资源使用情况的 HTML 页面
@app.get("/")
def read_root():
    results = {
        "时间": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        **get_cpu_usage(),
        **get_memory_usage(),
        **get_disk_usage(),
        **get_disk_io(),
        **get_process_count(),
        **get_thread_count(),
        **get_sleeping_process_count(),
        **get_top_cpu_processes(),
        **get_top_memory_processes()
    }
    return results

# 启动 FastAPI 应用程序
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("agent:app", host="0.0.0.0", port=8001, reload=True)
