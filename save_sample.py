# python save_sample.py
# 这样执行该脚本后，会在3秒后把左上角图标位置截取为截图，并保存为auto_png1.png
# 使用方法是，先执行脚本，然后3秒内打开游戏的对话界面，这样图标截图就保存下来了
# 然后应该把这两行代码注释掉，把下面的两行代码解除注释，然后再次做同样的动作，这样另一种状态的图标截图就保存下来了

from utils import *
import time

time.sleep(3)
img1=window_capture()
img1.save('auto_png1.png')

# img2=window_capture()
# img2.save('auto_png2.png')