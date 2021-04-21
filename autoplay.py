import ctypes
awareness = ctypes.c_int()
ctypes.windll.shcore.SetProcessDpiAwareness(2)
from mss import mss
from PIL import Image 
import win32ui, win32gui
import time

import keyboard, mouse

import ctypes, sys, os

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if os.path.basename(sys.executable.lower())[:6]!='python' and not is_admin():
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    exit()

def make_pycwnd(hwnd):       
    PyCWnd = win32ui.CreateWindowFromHandle(hwnd)
    return PyCWnd

def captureRect(rect):
    with mss() as sct:
        monitor = {"top": rect[0], "left": rect[1], "width": rect[2], "height": rect[3]}
        sct_img = sct.grab(monitor)
        # Convert to PIL/Pillow Image
        return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

def captureWindow(hwnd, local_rect=None):
    if local_rect is None:
        local_rect = win32gui.GetClientRect(hwnd)
    screen_rect = [*local_rect]
    screen_rect[:2] = win32gui.ClientToScreen(hwnd, local_rect[:2])
    screen_rect[2:] = win32gui.ClientToScreen(hwnd, local_rect[2:])
    return captureRect([screen_rect[1], screen_rect[0], screen_rect[2]-screen_rect[0], screen_rect[3]-screen_rect[1]])

def checkC(c):
    return c[0]>250 and c[1]>220 and c[2]<120

# def checkPix(img, pix, winsz = [0, 0, 2, 2]):
#     flag = False
#     for x in range(pix[0]-winsz[0], pix[0]+winsz[1]+1):
#         for y in range(pix[1]-winsz[2], pix[1]+winsz[3]+1):
#             flag = flag or checkC(img.getpixel((x, y)))
#     return flag

window_name = '原神'

hwnd = win32gui.FindWindow(None, window_name)

w,h = win32gui.GetClientRect(hwnd)[2:]

win32gui.ShowWindow(hwnd,5)
win32gui.SetForegroundWindow(hwnd)

left, top = win32gui.ClientToScreen(hwnd, (0,0))
time.sleep(0.5)

if w==0 or h==0:
    print("不支持独占全屏模式")
    exit()

if abs(w/h-1366/768)>0.05:
    print('请将原神设定成16:9分辨率')
    exit()

print('运行期间保持原神在前台，请勿遮挡窗口或操作鼠标')

inner_radius = int(48/1366*w)
outer_radius = int(56/1366*w)
mid_radius = int((inner_radius+outer_radius)/2)

def getRect(centers):
    x1, y1, x2, y2 = 99999999, 99999999, 0, 0
    for center in centers.values():
        x1 = min(x1, center[0])
        y1 = min(y1, center[1])
        x2 = max(x2, center[0])
        y2 = max(y2, center[1])
    
    return x1-outer_radius-1, y1-outer_radius-1, x2+outer_radius+1, y2+outer_radius+1

def checkKey(img, center):
    flag = False
    for x in [center[0]-outer_radius, center[0]+outer_radius]:
        flag = flag or checkC(img.getpixel((x, center[1])))
    for y in [center[1]-outer_radius, center[1]+outer_radius]:
        flag = flag or checkC(img.getpixel((center[0], y)))
    return flag


centers = {
    "a": (int(226/1366*w), int(460/768*h)), #A
    "w": (int(346/1366*w), int(341/768*h)), #W
    "d": (int(465/1366*w), int(460/768*h)), #D
    "s": (int(346/1366*w), int(580/768*h)), #S
    "j": (int(901/1366*w), int(460/768*h)), #J
    "i": (int(1021/1366*w), int(341/768*h)), #I
    "l": (int(1140/1366*w), int(460/768*h)), #L
    "k": (int(1021/1366*w), int(580/768*h)) #K
}

rect = getRect(centers)
print("检测区域",rect)
last_input_t = {key:0 for key in centers.keys()}
# ahk = AHK()
i = 0
total = 0
maxt = 0
mint = 99999999
smooth_thres = 0.25
while True:
    start = time.time()
    img = captureWindow(hwnd, rect)

    to_input = ''

    for key, center in centers.items():
        if checkKey(img, (center[0]-rect[0], center[1]-rect[1])):
            if start-last_input_t[key]>smooth_thres:
                to_input += key
                last_input_t[key] = start
    if to_input:
        keyboard.press_and_release(list(to_input))
    cur_t =  time.time()-start
    total += cur_t
    maxt = max(cur_t, maxt)
    mint = min(cur_t, mint)
    i += 1
    print("平均每帧 {:.4f}s, 最大 {:.4f}s, 最小 {:.4f}s".format(total/i, maxt, mint), end='\r')
    
