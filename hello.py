import time
import sys
import json
import psutil
import socket
import uuid
import subprocess
import os
import pygame
import random

# 定义不同语言的提示信息
messages = {
    'en': 'Your computer will be locked in {} minute(s).',
    'zh': '您的计算机将在{}分钟后被锁定。',
    'fil': 'Ang iyong computer ay maaaring ma-lock sa loob ng {} minuto.',
    'ko': '당신의 컴퓨터가 {}분 후에 잠길 것입니다.',
    'ja': 'あなたのコンピュータは{}分後にロックされます。',
    'default': 'Your computer will be locked in {} minute(s).'
}

# 获取当前系统语言
def get_system_language():
    system_language = 'en'  # 默认为英语
    if sys.platform.startswith('win'):
        import ctypes
        system_language = ctypes.windll.kernel32.GetUserDefaultUILanguage()
    elif sys.platform == 'darwin':
        import subprocess
        output = subprocess.check_output(['defaults', 'read', '-g', 'AppleLanguages'])
        system_language = output.decode().strip().split('"')[1][:2]
    print("System language: ", system_language)
    return system_language

# 获取系统内网IP地址和MAC地址
def get_network_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
    return {'hostname': hostname, 'ip_address': ip_address, 'mac_address': mac_address}

# 获取当前用户和登录用户信息
def get_user_info():
    current_user = subprocess.check_output("whoami").strip().decode()
    logged_users = subprocess.check_output("w").strip().decode()
    return {'current_user': current_user, 'logged_users': logged_users}

# 获取系统CPU使用率
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

# 获取系统内存使用率
def get_memory_usage():
    return psutil.virtual_memory().percent

# 获取系统磁盘使用率
def get_disk_usage():
    return psutil.disk_usage('/').percent

# 获取系统磁盘读写速度
def get_disk_io():
    return psutil.disk_io_counters()

# 锁定键盘鼠标，需要输入特定密码才能解除锁定，或者网吧管理员远程解除锁定
def lock_keyboard_mouse():
    # 实现锁定键盘鼠标的逻辑
    pass

# 弹出提醒
def show_notification(message):
    print(message)  # 实时输出运行日志
    if sys.platform == 'win32':
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, message, 'Reminder', 0x40)
    elif sys.platform == 'darwin':
        import subprocess
        subprocess.run(['osascript', '-e', 'display notification "{}" with title "Reminder"'.format(message)])

# 黑客代码雨特效
def hacker_rain(screen, font, font_size, drop_positions):
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    GREEN = (0, 255, 0)
    for i, position in enumerate(drop_positions):
        char = random.choice(chars)
        text = font.render(char, True, GREEN)
        screen.blit(text, (i * font_size, position))
        drop_positions[i] = (position + font_size) % 1920  # 更新位置，使得文字下落

# 主函数
def main(minutes):
    system_language = get_system_language()
    for i in range(minutes, 0, -1):
        message = messages.get(system_language, messages['default']).format(i)
        show_notification(message)
        network_info = get_network_info()
        user_info = get_user_info()
        cpu_usage = get_cpu_usage()
        memory_usage = get_memory_usage()
        disk_usage = get_disk_usage()
        disk_io = get_disk_io()
        log_data = {
            'message': message,
            'network_info': network_info,
            'user_info': user_info,
            'cpu_usage': cpu_usage,
            'memory_usage': memory_usage,
            'disk_usage': disk_usage,
            'disk_io': disk_io
        }
        print(json.dumps(log_data, indent=4))  # 将日志以JSON格式打印输出
        
        # 判断时间差异，如果小于3分钟，显示代码雨效果持续10秒
        current_minutes = i
        if current_minutes <= 3:
            pygame.time.set_timer(pygame.USEREVENT, 10000)  # 设置事件定时器，持续10秒
            font_size = 15
            drop_positions = [random.randint(0, 800) for _ in range(1920 // font_size)]
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.USEREVENT:
                        break
                screen.fill((0, 0, 0))  # 清空屏幕
                hacker_rain(screen, font, font_size, drop_positions)
                pygame.display.flip()  # 更新屏幕显示
                pygame.time.delay(20)  # 延迟20毫秒
                if event.type == pygame.USEREVENT:
                    break
        
        time.sleep(60)  # 等待一分钟

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Hacker Rain")
font = pygame.font.SysFont("Courier", 15, bold=True)

if __name__ == "__main__":
    minutes = int(input("Enter the number of minutes: "))
    main(minutes)
