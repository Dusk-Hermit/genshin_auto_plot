# 用此脚本来获取3秒内的鼠标位置

import win32api
import time

for i in range(50):
    time.sleep(0.1)
    print(f'mouse position:{win32api.GetCursorPos()}')