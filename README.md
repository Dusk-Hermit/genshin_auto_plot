## 原神自动过剧情脚本

### 环境

```cmd
pip install -r requirements.txt
```
在你自己的python环境中用此命令安装依赖包

### 功能

主程序在`utils.py`。
打开`run.bat`脚本后，会尝试获取管理员权限，以保证点击和鼠标移动的正常执行

程序每1秒进行一次检测，如果鼠标此时在屏幕最右下角位置，则暂停下述功能，如果鼠标此时在屏幕最右上角位置，则开启下述功能：

每秒检测屏幕左上角对应位置是否有原神对话的开始图标![alt text](auto_png1.png)或者暂停图标![alt text](auto_png2.png)
有的话，就把鼠标移动到某个位置进行点击，再恢复鼠标原位置

上述的点击位置在`utils.py`定义为`CLICK_POINT`，个人设置为某个对话选项会出现的位置，这样能自动点击剧情选项了
可以执行这个脚本，来快速查看当前鼠标的位置
```cmd
python get_mouse.py
```

现在的预设是2k屏幕的，如果你的屏幕不是2k分辨率的，则需要修改![alt text](auto_png1.png)和![alt text](auto_png2.png)，以及`utils.py`中的`X1,X2,Y1,Y2`
*现在已支持1080p屏幕*
你可以用随便什么方法，来获得你的屏幕上这两个图标会出现的位置。`X1,X2,Y1,Y2`分别是这个位置框的左边缘、右边缘到屏幕最左侧的距离，以及位置框的上边缘、下边缘到屏幕最上侧的距离，单位为像素
修改变量之后，你可以用自己的软件，截取原神中对话过程下屏幕的该位置框内的图片，以替换这里的两个png文件，也可以用`save_sample.py`来帮你完成


### 问题

- 如果遇到剧情选项没有成功执行鼠标点击，可以看一下控制台的相似度计算，把`utils.py`中的相似度阈值往下调一些