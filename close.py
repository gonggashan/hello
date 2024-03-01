# coding: UTF-8
import time
from ctypes import *
user32 = windll.LoadLibrary('user32.dll')
user32.BlockInput(True);
time.sleep(50);
user32.BlockInput(False);