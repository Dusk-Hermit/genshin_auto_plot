import time
import win32gui, win32ui, win32con, win32api
from PIL import Image
import cv2
import numpy as np
import random
import ctypes
import sys

img1=Image.open('auto_png1.png')
img2=Image.open('auto_png2.png')

print(f'img1.size:{img1.size}')
print(f'img2.size:{img2.size}')

assert img1.size==img2.size

img1_cv=cv2.cvtColor(np.array(img1), cv2.COLOR_RGB2BGR)
img2_cv=cv2.cvtColor(np.array(img2), cv2.COLOR_RGB2BGR)

MoniterDev = win32api.EnumDisplayMonitors(None, None)
SCREEN_WIDTH = MoniterDev[0][2][2]
SCREEN_HEIGHT = MoniterDev[0][2][3]

THRESHOLD=0.9
CLICK_POINT=(1817, 1069)
X1,X2,Y1,Y2=80,110,45,80

def window_capture(x=X1,y=Y1,width=X2-X1,height=Y2-Y1):
    
    time_start = time.time()
    hwnd = 0
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    
    # print(w,h)
    
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (width, height),  mfcDC,(x,y),win32con.SRCCOPY)
    
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    # 创建PIL的Image对象
    img = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1
    )
    
    print('Time spent on screen capturing:', round(1000*(time.time()-time_start),1) ,'ms')

    return img


def calculate_similarity(image1, image2):
 
    # 初始化ORB检测器
    orb = cv2.ORB_create()

    # 寻找特征点和描述符
    kp1, des1 = orb.detectAndCompute(image1, None)
    kp2, des2 = orb.detectAndCompute(image2, None)

    # 初始化BFMatcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # 进行特征点匹配
    matches = bf.match(des1, des2)

    # 按照距离排序
    matches = sorted(matches, key=lambda x: x.distance)

    # 计算相似度
    similarity = len(matches)

    return similarity/len(kp1)


def mainloop():
    img_temp=window_capture()
    img_temp_cv=cv2.cvtColor(np.array(img_temp), cv2.COLOR_RGB2BGR)

    #模板匹配
    result_1 = cv2.matchTemplate(img_temp_cv, img1_cv, cv2.TM_CCOEFF_NORMED)
    result_2 = cv2.matchTemplate(img_temp_cv, img2_cv, cv2.TM_CCOEFF_NORMED)
    min_max_1 = cv2.minMaxLoc(result_1)  #计算匹配度
    min_max_2 = cv2.minMaxLoc(result_2)  #计算匹配度
    
    score=max(min_max_1[1],min_max_2[1])
    
    print(f'Similarity :{round(score*100,2)} %')
    
    # 如果匹配度很高，则认为当前是对话状态，鼠标会移动到指定位置，然后模拟鼠标单击
    if score > THRESHOLD :
        return True
    else:
        return False

def click_and_restore():
    temp=win32api.GetCursorPos()
    
    print('clicked now')
    
    # win32api.SetCursorPos(CLICK_POINT)
    ctypes.windll.user32.SetCursorPos(*CLICK_POINT)
    
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    ctypes.windll.user32.mouse_event(2)
    
    time.sleep(0.1 + 0.1 * random.random())
    
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
    ctypes.windll.user32.mouse_event(4)
    
    time.sleep(0.1)
    
    # win32api.SetCursorPos(temp)
    ctypes.windll.user32.SetCursorPos(*temp)

def warpper():
    if ctypes.windll.shell32.IsUserAnAdmin() :
        print('当前已是管理员权限')
        main()
    else:
        print('当前不是管理员权限，以管理员权限启动新进程...')
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

def main():
    # 如果鼠标在右下角，则暂停程序的功能
    # 如果鼠标在右上角，则重新启动程序的功能
    state_on=True
    while True:
        
        cursor_pos=win32api.GetCursorPos()
        if cursor_pos==(SCREEN_WIDTH-1,SCREEN_HEIGHT-1):
            state_on=False
            print('鼠标在右下角，暂停程序')
        elif cursor_pos==(SCREEN_WIDTH-1,0):
            state_on=True
            print('鼠标在右上角，重新启动程序')
        
        if state_on:
            if mainloop():
                click_and_restore()
   
        time.sleep(1)

if __name__ == '__main__':
    warpper()