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

# 获取当前系统语言
def 获取系统语言():
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

# 获取系统内网IP地址和MAC地址
def 获取网络信息():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
    return {'主机名': hostname, 'IP地址': ip_address, 'MAC地址': mac_address}

# 获取当前用户和登录用户信息
def 获取用户信息():
    current_user = subprocess.check_output("whoami").strip().decode()
    logged_users = subprocess.check_output("w").strip().decode()
    return {'当前用户': current_user, '登录用户': logged_users}

# 获取系统CPU使用率
def 获取CPU使用率():
    return psutil.cpu_percent(interval=1)

# 获取系统内存使用率
def 获取内存使用率():
    return psutil.virtual_memory().percent

# 获取系统磁盘使用率
def 获取磁盘使用率():
    return psutil.disk_usage('/').percent

# 获取系统磁盘读写速度
def 获取磁盘IO():
    return psutil.disk_io_counters()

# 弹出提醒
def 弹出通知(message):
    if sys.platform == 'darwin':
        # 在 macOS 上显示持续对话框
        subprocess.run(['osascript', '-e', f'display dialog "{message}" with title "Reminder!!!" buttons {{"OK"}} default button "OK" with icon note giving up after 9999'])
    elif sys.platform.startswith('win'):
        # 在 Windows 上显示持续消息框
        ctypes.windll.user32.MessageBoxW(0, message, "Reminder!!!", 0x40)
    else:
        print("Unsupported platform for notifications")

# 主函数
def 主程序(分钟数):
    system_language = 获取系统语言()
    
    # 获取结束时间
    end_time = datetime.now() + timedelta(minutes=分钟数)
    
    while datetime.now() < end_time:
        # 判断当前时间和结束时间的差值
        time_difference = end_time - datetime.now()
        current_minutes = time_difference.total_seconds() // 60
        
        # 每分钟输出日志
        if current_minutes < 5:
            message = messages.get(system_language, messages['default']).format(int(current_minutes))
            弹出通知(message)
            
            # 输出日志到命令行
            network_info = 获取网络信息()
            user_info = 获取用户信息()
            cpu_usage = 获取CPU使用率()
            memory_usage = 获取内存使用率()
            disk_usage = 获取磁盘使用率()
            disk_io = 获取磁盘IO()
            log_data = {
                '消息': message,
                '网络信息': network_info,
                '用户信息': user_info,
                'CPU使用率': cpu_usage,
                '内存使用率': memory_usage,
                '磁盘使用率': disk_usage,
                '磁盘IO': disk_io
            }
            print(json.dumps(log_data, indent=4))
        
        time.sleep(60)  # 等待一分钟

if __name__ == "__main__":
    分钟数 = int(input("请输入分钟数: "))
    主程序(分钟数)
