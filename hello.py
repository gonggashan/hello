import time
import sys
import json
import psutil
import socket
import uuid
import subprocess
from datetime import datetime, timedelta
import ctypes

# 定义不同语言的提示信息
messages = {
    'en': 'Your computer will be locked in {} minute(s). Please contact the cyber cafe administrator for recharge',
    'zh': '您的计算机将在{}分钟后被锁定。请联系网吧管理员充值',
    'fil': 'Ang iyong computer ay maaaring ma-lock sa loob ng {} minuto. Mangyaring makipag-ugnayan sa administrator ng internet cafe para sa pagpapalit ng singil.',
    'ko': '컴퓨터가 {}분 후에 잠길 것입니다. 충전을 위해 사이버 카페 관리자에게 문의하십시오.',
    'ja': 'あなたのコンピュータは{}分後にロックされます。充電のためにサイバーカフェの管理者にお問い合わせください。',
    'ms': 'Komputer anda akan dikunci dalam {} minit. Sila hubungi pentadbir kafe cyber untuk tambah nilai',
    'ru': 'Ваш компьютер будет заблокирован через {} минут(ы). Пожалуйста, свяжитесь с администратором киберкафе для пополнения',
    'id': 'Komputer Anda akan terkunci dalam {} menit. Silakan hubungi administrator kafe internet untuk mengisi ulang',
    'zh_TW': '您的電腦將在{}分鐘後被鎖定。請聯繫網咖管理員進行充值',
    'vi': 'Máy tính của bạn sẽ bị khóa trong {} phút. Vui lòng liên hệ với quản trị viên quán internet để nạp tiền',
    'default': 'Your computer will be locked in {} minute(s). Please contact the cyber cafe administrator for recharge'
}

# 获取系统语言
def get_system_language():
    system_language = 'en'  # 默认为英语
    if sys.platform.startswith('win'):
        import ctypes
        system_language = ctypes.windll.kernel32.GetUserDefaultUILanguage()
    elif sys.platform == 'darwin':
        import subprocess
        output = subprocess.check_output(['defaults', 'read', '-g', 'AppleLanguages'])
        system_language = output.decode().strip().split('"')[1][:2]
    print("系统语言: ", system_language)
    return system_language

# 获取网络信息
def get_network_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
    return {'主机名': hostname, 'IP地址': ip_address, 'MAC地址': mac_address}

# 获取用户信息
def get_user_info():
    current_user = subprocess.check_output("whoami").strip().decode()
    logged_users = subprocess.check_output("w").strip().decode()
    return {'当前用户': current_user, '登录用户': logged_users}

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

# 弹出通知
def show_notification(message):
    if sys.platform == 'darwin':
        # 在 macOS 上显示持续对话框
        subprocess.run(['osascript', '-e', f'display dialog "{message}" with title "Reminder!!!" buttons {{"OK"}} default button "OK" with icon note giving up after 9999'])
    elif sys.platform.startswith('win'):
        # 在 Windows 上显示持续消息框
        ctypes.windll.user32.MessageBoxW(0, message, "Reminder!!!", 0x40)
    else:
        print("Unsupported platform for notifications")

# 主程序
def main(minutes):
    system_language = get_system_language()
    end_time = datetime.now() + timedelta(minutes=minutes)
    
    while datetime.now() < end_time:
        time_difference = end_time - datetime.now()
        current_minutes = time_difference.total_seconds() // 60
        
        if current_minutes < 5:
            network_info = get_network_info()
            user_info = get_user_info()
            cpu_usage = get_cpu_usage()
            memory_usage = get_memory_usage()
            disk_usage = get_disk_usage()
            disk_io = get_disk_io()
            process_count = get_process_count()
            thread_count = get_thread_count()
            sleeping_process_count = get_sleeping_process_count()
            top_10_cpu_processes = get_top_cpu_processes()  # 修正此处调用
            top_10_memory_processes = get_top_memory_processes()
            
            log_data = {
                '消息': message,
                '网络信息': network_info,
                '用户信息': user_info,
                'CPU使用率': cpu_usage,
                '内存使用率': memory_usage,
                '磁盘使用率': disk_usage,
                '磁盘IO': disk_io._asdict(),  # 将命名元组转换为字典
                '进程数量': process_count,
                '线程数量': thread_count,
                '沉睡进程数量': sleeping_process_count,
                '最占CPU前10进程': top_10_cpu_processes,
                '最占内存前10进程': top_10_memory_processes
            }
            print(json.dumps(log_data, ensure_ascii=False, indent=4))  # 确保输出中文和表情符号正常显示
            message = messages.get(system_language, messages['default']).format(int(current_minutes))
            show_notification(message)
        
        time.sleep(60)  # 等待一分钟

if __name__ == "__main__":
    minutes = int(input("请输入分钟数: "))
    main(minutes)
