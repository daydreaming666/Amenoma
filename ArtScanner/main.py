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
from utils import decodeValue, findWindowsByName, calcFormatWidth, setWindowToForeground

if len(sys.argv)>1:
    bundle_dir = sys.argv[1]
else:
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

import win32gui

window_name_cn = '原神'
while True:
    windows = findWindowsByName(window_name_cn)
    if len(windows) == 0:
        window_name_cn = input('未找到在运行的原神，请在这里输入窗口标题（留空则列出所有尺寸非0窗口）：').strip().lower()
    elif len(windows) == 1:
        hwnd = windows[0][0]
        break
    else:
        print('-----------------------------')
        print(f'发现多个窗口名为{window_name_cn}，请从以下列表中选择：')
        print('{0:^{4}} {1:^{5}} {2:^{6}} {3:^{7}}'.format('编号','窗口标题', '进程名', '窗口内部分辨率',
            calcFormatWidth('编号', 5), calcFormatWidth('窗口标题', 25), calcFormatWidth('进程名', 25), calcFormatWidth('窗口内部分辨率', 15)))
        for i, window in enumerate(windows):
            print('{0:^5} {1:<{4}.{4}} {2:<{5}.{5}} {3:<15}'.format(i+1, window[1], os.path.basename(window[2]), str(window[3]), 
                calcFormatWidth(window[1], 25), calcFormatWidth(window[2], 25)))
        hwnd = windows[int(input('请输入要选择的编号：'))-1][0]
        print('-----------------------------')
        break

game_info = GameInfo(hwnd)

if game_info.w==0 or game_info.h==0:
    print("不支持独占全屏模式")
    game_info.w, game_info.h = eval(input("如果要尝试继续运行，请输入原神的分辨率，格式是\"宽,高\"，例如 1920,1080（不用引号）："))
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
ocr_model = ocr.OCR(scale_ratio=game_info.scale_ratio, model_weight=os.path.join(bundle_dir, 'mn_model_weight.h5'))
art_id = 0
saved = 0
skipped = 0
failed = 0
star_dist = [0,0,0,0,0]
star_dist_saved = [0,0,0,0,0]


os.makedirs('artifacts', exist_ok=True)

input('请打开圣遗物背包界面，最好翻到圣遗物列表最上面。按回车继续')
print('---------------------------------')
if game_info.incomplete_lastrow:
    input(f'检测到圣遗物背包有{game_info.art_rows}行{game_info.art_cols}列，但最后一行不完整可能会影响自动翻页效果，建议更改分辨率到16:9')
else:
    input(f'自动判断圣遗物背包有{game_info.art_rows}行{game_info.art_cols}列，请务必确认是否正确！！错误请退出并更改分辨率后尝试')
print('---------------------------------')
input('运行期间请保持原神在前台，请勿遮挡窗口或操作鼠标，按鼠标中键停止。按回车继续')
input('开始后将尝试自动对齐第一行以方便识别，若对齐结果有误，请立刻按中键停止。按回车继续')
print('---------------------------------')
if input('是否进行高级设置，例如等级过滤，稀有度过滤，翻页延迟，导出格式，确认请输入y：').strip().lower()=='y':
    export_type = input('请输入需要的导出格式，0=莫娜的占卜铺（回车默认值），1=MingyuLab。')
    level_threshold = input('请输入圣遗物等级阈值(0-20)(比如：16，则仅将保存16级及以上的圣遗物信息)。直接按回车则默认保存所有圣遗物信息。')
    rarity_threshold = input('请输入圣遗物星级阈值(1-5)(比如：5，则仅将保存5星的圣遗物信息)。直接按回车则默认保存所有圣遗物信息。')
    scroll_interval = input('请输入翻页时的检测延迟（秒），数值越大翻页速度越慢，可以解决一些翻页时的检测BUG，直接回车则为默认值0.05。')
print('---------------------------------')
print('程序将于5秒后自动开始运行，若此条提示显示时未自动切换到原神窗口，请手动点击原神窗口切到前台')

setWindowToForeground(hwnd)

time.sleep(5)

art_scanner = ArtScannerLogic(game_info)
art_data = ArtDatabase('artifacts.dat')

try:
    level_threshold = int(level_threshold)
except:
    level_threshold = 0
try:
    rarity_threshold = int(rarity_threshold)
except:
    rarity_threshold = 0
try:
    scroll_interval = float(scroll_interval)
except:
    scroll_interval = 0.05
try:
    exporter = [art_data.exportGenshinArtJSON, art_data.exportMingyuLabJSON][int(export_type)]
    export_name = ['artifacts.genshinart.json', 'artifacts.mingyulab.json'][int(export_type)]
except:
    exporter = art_data.exportGenshinArtJSON
    export_name = 'artifacts.genshinart.json'


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
    global star_dist
    info = ocr_model.detect_info(art_img)
    star_dist[info['star']-1] += 1
    if decodeValue(info['level'])<level_threshold or decodeValue(info['star'])<rarity_threshold:
        skipped += 1
    elif art_data.add(info, art_img):
        saved += 1
        star_dist_saved[info['star']-1] += 1
    else:
        art_img.save(f'artifacts/{art_id}.png')
        s = json.dumps(info, ensure_ascii=False)
        with open(f"artifacts/{art_id}.json", "wb") as f:
            f.write(s.encode('utf-8'))
        failed += 1
    art_id += 1
    print(f"\r已扫描{art_id}个圣遗物，已保存{saved}个，已跳过{skipped}个，游戏平均响应时间{art_scanner.avg_response_time*1000:3.0f}毫秒", end='')

try:
    while True:
        if art_scanner.stopped or not art_scanner.scanRows(rows=range(start_row, game_info.art_rows), callback=artscannerCallback) or start_row!=0:
            break
        start_row = game_info.art_rows-art_scanner.scrollToRow(game_info.art_rows, max_scrolls=20, extra_scroll=int(game_info.art_rows>5), interval=scroll_interval)
        if start_row==game_info.art_rows:
            break
    print()
    if art_scanner.stopped:
        print("用户已中断扫描")
    elif start_row!=0:
        print("没有检测到下一页圣遗物，自动终止")
    else:
        print("在最后点击位置未检测到圣遗物，自动终止")
except Exception as e:
    print()
    print(f"因为\"{repr(e)}\"而意外停止扫描，将保存已扫描的圣遗物信息")
if saved != 0:
    exporter(export_name)
print(f'总计扫描了{skipped+saved}/{art_id}个圣遗物，保存了{saved}个到{export_name}，失败了{failed}个')
print('无效识别/失败结果请到artifacts路径中查看')
print('----------------------------')
print('圣遗物星级分布：（保存数量/扫描数量）')
print(f'5星：{star_dist_saved[4]}/{star_dist[4]}')
print(f'4星：{star_dist_saved[3]}/{star_dist[3]}')
print(f'3星：{star_dist_saved[2]}/{star_dist[2]}')
print(f'2星：{star_dist_saved[1]}/{star_dist[1]}')
print(f'1星：{star_dist_saved[0]}/{star_dist[0]}')
print('----------------------------')
input('已完成，按回车退出')