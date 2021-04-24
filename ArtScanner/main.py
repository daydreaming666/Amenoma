import ctypes, sys
# awareness = ctypes.c_int()
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
        print('检测到不支持进程DPI设置（可能是系统版本低于Win10）')
        print('程序将会继续执行，但在高分屏上可能存在分辨率问题')
    except:
        print('检测到不支持读取系统DPI设置（可能是系统版本低于Win8）')
        print('程序将会继续执行，但在高分屏上可能存在分辨率问题')

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
#os.path.basename(sys.executable.lower())[:6]!='python' and 
if not is_admin():
    # Re-run the program with admin rights
    # ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv+[bundle_dir]), None, 1)
    input('请在右键菜单选择以管理员模式运行')
    sys.exit(0)

import win32gui
import time
import keyboard, mouse
import os
import json
import ocr
from art_saver import ArtDatabase
from art_scanner_logic import ArtScannerLogic, GameInfo
from utils import decodeValue

if len(sys.argv)>1:
    bundle_dir = sys.argv[1]
else:
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))


window_name_cn = '原神'
hwnd = win32gui.FindWindow(None, window_name_cn)
    
if hwnd is None or hwnd==0:
    input('未找到在运行的原神')
    sys.exit(0)

game_info = GameInfo(hwnd)

if game_info.w==0 or game_info.h==0:
    print("不支持独占全屏模式")
    game_info.w, game_info.h = eval(input("如果要强行继续运行，请输入原神的分辨率，格式是\"宽,高\"，例如 1920,1080（不用引号）："))
    game_info.left, game_info.top = 0, 0

game_info.calculateCoordinates()

# print(art_cols, art_rows)
# import win32api, win32ui
# dc = win32gui.GetDC(0)
# dcObj = win32ui.CreateDCFromHandle(dc)
# hwnd = win32gui.WindowFromPoint((0,0))
# red = win32api.RGB(255, 0, 0)
# monitor = (0, 0, win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))
# while True:
#     dcObj.Rectangle((int(left+first_art_x), int(top+first_art_y), int(left+first_art_x)+10, int(top+first_art_y)+10))
#     dcObj.Rectangle((int(left+art_info_left), int(top+art_info_top), int(left+art_info_left)+10, int(top+art_info_top)+10))
#     dcObj.Rectangle((int(left+art_info_left+art_info_width), int(top+art_info_top+art_info_height), int(left+art_info_left+art_info_width)+10, int(top+art_info_top+art_info_height)+10))
#     dcObj.Rectangle((int(left+scroll_keypt_x), int(top+scroll_keypt_y), int(left+scroll_keypt_x)+10, int(top+scroll_keypt_y)+10)) 
#     win32gui.InvalidateRect(hwnd, monitor, True)

# # star color=255,204,50
# scroll_fin_keypt_x = 358
# scroll_fin_keypt_y = 320

# margin near level number, color=233,229,220

# initialization
ocr_model = ocr.OCR(scale_ratio=game_info.scale_ratio, model_path=os.path.join(bundle_dir, 'mn_model.h5'))
art_id = 0
saved = 0
skipped = 0
failed = 0

os.makedirs('artifacts', exist_ok=True)

input('请打开圣遗物背包界面，最好翻到圣遗物列表最上面。按回车继续')
if game_info.incomplete_lastrow:
    input(f'检测到圣遗物背包有{game_info.art_rows}行{game_info.art_cols}列，但最后一行不完整可能会影响自动翻页效果，建议更改分辨率到16:9')
else:
    input(f'自动判断圣遗物背包有{game_info.art_rows}行{game_info.art_cols}列，请务必确认是否正确！！错误请退出并更改分辨率后尝试')
input('运行期间请保持原神在前台，请勿遮挡窗口或操作鼠标，按鼠标中键停止。按回车继续')
input('开始后将尝试自动对齐第一行以方便识别，若对齐结果有误，请立刻按中键停止。按回车继续')
level_threshold = input('请输入圣遗物等级阈值(0-20)(比如：16，则仅将保存16级及以上的圣遗物信息)。直接按回车则默认保存所有圣遗物信息。')
print('程序将于5秒后自动开始运行，若此条提示显示时未自动切换到原神窗口，请手动点击原神窗口切到前台')

try:
    level_threshold = int(level_threshold)
except ValueError:
    level_threshold = 0

keyboard.press('alt')
win32gui.ShowWindow(hwnd,5)
win32gui.SetForegroundWindow(hwnd)
keyboard.release('alt')

time.sleep(5)

art_scanner = ArtScannerLogic(game_info)
art_data = ArtDatabase('artifacts.dat')
mouse.on_middle_click(art_scanner.interrupt)

print('正在自动对齐')
art_scanner.alignFirstRow()
print('对齐完成，即将开始扫描')
time.sleep(0.5)
start_row = 0

def artscannerCallback(art_img):
    global saved
    global art_id
    global skipped
    global failed
    info = ocr_model.detect_info(art_img)
    if decodeValue(info['level'])<level_threshold:
        skipped += 1
    elif art_data.add(info, art_img):
        saved += 1
    else:
        art_img.save(f'artifacts/{art_id}.png')
        s = json.dumps(info)
        with open(f"artifacts/{art_id}.json", "wt") as f:
            f.write(s)
        failed += 1
    art_id += 1
    print(f"\r已扫描{art_id}个圣遗物，已保存{saved}个，已跳过{skipped}个", end='')

try:
    while True:
        if art_scanner.stopped or not art_scanner.scanRows(rows=range(start_row, game_info.art_rows), callback=artscannerCallback) or start_row!=0:
            break
        start_row = game_info.art_rows-art_scanner.scrollToRow(game_info.art_rows, max_scrolls=20, extra_scroll=int(game_info.art_rows>5))
        if start_row==game_info.art_rows:
            break
    print()
    if art_scanner.stopped:
        print("用户已中断扫描")
    elif start_row==game_info.art_rows:
        print("没有检测到下一页圣遗物，自动终止")
    else:
        print("在最后点击位置未检测到圣遗物，自动终止")
except Exception as e:
    raise
    print()
    print(f"因为\"{e}\"而意外停止扫描，将保存已扫描的圣遗物信息")
if saved != 0:
    art_data.exportGenshinArtJSON('artifacts.genshinart.json')
print(f'总计扫描了{skipped+saved}/{art_id}个圣遗物，保存了{saved}个到artifacts.genshinart.json，失败了{failed}个')
print('无效识别/失败结果请到artifacts路径中查看')
input('已完成，按回车退出')