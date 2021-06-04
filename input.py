# -- coding: utf-8 --
from pymouse import *     # 模拟鼠标所使用的包
from pykeyboard import *   # 模拟键盘所使用的包
import pyperclip
import time   # 连续进行两个动作可能太快而效果不明显，因此加入暂停时间
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
m = PyMouse()   # 鼠标的实例m
k = PyKeyboard()   # 键盘的实例k
x_dim, y_dim = m.screen_size()     # 获取屏幕尺寸（一般为电脑屏幕的分辨率，如1920*1080）
# 估计需要点击的位置坐标（不知道有没有定位代码，我没找到，我是自己估计的。例如，我的电脑屏幕为(1920，1080)，我想要单击的地方估计坐标为(10，500)）
m.move(1000, 5000)   # 将鼠标移动到位（此步可忽略，直接单击也可）
time.sleep(0.5)   # 暂停0.5s，方便观察移动结果
m.click(1000, 400, 1, 1)   # 表示在(10, 500)的地方，单击左键
#k.type_string('rizai')   # 模拟键盘输入字符串
pyperclip.copy("#中文")
#time.sleep(2)
k.press_key(k.control_key) #–模拟键盘按H键 
k.press_key('v') #–模拟键盘松开
k.release_key('v')#中文#中文
k.release_key(k.control_key)#此时，汉字已经被复制到输入框了