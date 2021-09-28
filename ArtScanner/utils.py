import keyboard
import unicodedata
import win32api
import win32con
import win32gui
import win32process
from PIL import Image
from mss import mss
import Levenshtein
import ArtsInfo
import logging

logger = logging.getLogger()
logHandler = logging.FileHandler("./Amenoma.log", encoding='utf-8')
logHandler.setFormatter(logging.Formatter("[%(levelname)7s] %(asctime)s /%(module)10s[%(lineno)3d]\t"
                                          "/%(message)s"))
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

def calcFormatWidth(text, target):
    return target - sum(unicodedata.east_asian_width(c) in 'WF' for c in text)


def setWindowToForeground(hwnd):
    keyboard.press('alt')
    win32gui.ShowWindow(hwnd, 5)
    win32gui.SetForegroundWindow(hwnd)
    keyboard.release('alt')


def getProcessName(hwnd):
    try:
        pid = win32process.GetWindowThreadProcessId(hwnd)
        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid[1])
        return win32process.GetModuleFileNameEx(handle, 0)
    except:
        return "Unknown"


def findWindowsByName(name):
    windows = []

    def winEnumHandler(hwnd, ctx):
        win_name = win32gui.GetWindowText(hwnd)
        win_size = win32gui.GetClientRect(hwnd)[2:]
        if win32gui.IsWindowVisible(hwnd) and name in win_name and ((win_size[0] * win_size[1]) != 0 or len(name) > 0):
            windows.append((hwnd, win_name, getProcessName(hwnd), win_size))

    win32gui.EnumWindows(winEnumHandler, None)
    return windows


def captureRect(rect):
    with mss() as sct:
        monitor = {"top": rect[0], "left": rect[1], "width": rect[2], "height": rect[3]}
        sct_img = sct.grab(monitor)
        # Convert to PIL/Pillow Image
        return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')


def captureWindow(hwnd, local_rect=None):
    if local_rect is None:
        local_rect = win32gui.GetClientRect(hwnd)
    else:
        local_rect = tuple([int(round(i)) for i in local_rect])
    screen_rect = [*local_rect]
    screen_rect[:2] = win32gui.ClientToScreen(hwnd, local_rect[:2])
    screen_rect[2:] = win32gui.ClientToScreen(hwnd, local_rect[2:])
    return captureRect(
        [screen_rect[1], screen_rect[0], screen_rect[2] - screen_rect[0], screen_rect[3] - screen_rect[1]])


def decodeValue(v):
    if type(v) != str:
        return v
    if "%" in v:
        return float(v[:-1]) / 100
    else:
        return int(v.replace(',', '').replace('+', ''))


def attr_auto_correct(attr: str) -> str:
    corr_name = ''
    dis = 10000000
    for n in ArtsInfo.MainAttrNames.values():
        ndis = Levenshtein.distance(attr, n)
        if ndis < dis:
            dis = ndis
            corr_name = n
    if dis == 0:
        pass
    elif dis <= (len(attr) // 3):
        logger.info(f"Corrected attribute from [{attr}] to [{corr_name}] with distance {dis}")
    else:
        logger.warning(f"Corrected attribute from [{attr}] to [{corr_name}] with distance {dis}")
    return corr_name


def name_auto_correct(name: str) -> str:
    corr_name = ""
    dis = 10000000
    for arts in ArtsInfo.ArtNames:
        for rname in arts:
            ndis = Levenshtein.distance(name, rname)
            if ndis < dis:
                corr_name = rname
                dis = ndis
    if dis == 0:
        pass
    elif dis <= (len(name) // 3):
        logger.info(f"Corrected name from [{name}] to [{corr_name}] with distance {dis}")
    else:
        logger.warning(f"Corrected name from [{name}] to [{corr_name}] with distance {dis}")
    return corr_name


def attr_auto_correct_EN(attr: str) -> str:
    corr_name = ''
    dis = 10000000
    for n in ArtsInfo.MainAttrNames_EN.values():
        ndis = Levenshtein.distance(attr, n)
        if ndis < dis:
            dis = ndis
            corr_name = n
    if dis == 0:
        pass
    elif dis <= (len(attr) // 3):
        logger.info(f"Corrected attribute from [{attr}] to [{corr_name}] with distance {dis}")
    else:
        logger.warning(f"Corrected attribute from [{attr}] to [{corr_name}] with distance {dis}")
    return corr_name


def name_auto_correct_EN(name: str) -> str:
    corr_name = ""
    dis = 10000000
    for arts in ArtsInfo.ArtNames_EN:
        for rname in arts:
            ndis = Levenshtein.distance(name, rname)
            if ndis < dis:
                corr_name = rname
                dis = ndis
    if dis == 0:
        pass
    elif dis <= (len(name) // 3):
        logger.info(f"Corrected name from [{name}] to [{corr_name}] with distance {dis}")
    else:
        logger.warning(f"Corrected name from [{name}] to [{corr_name}] with distance {dis}")
    return corr_name


def type_auto_correct(name: str) -> str:
    corr_name = ""
    dis = 10000000
    for arts in ArtsInfo.TypeNames:
        for rname in arts:
            ndis = Levenshtein.distance(name, rname)
            if ndis < dis:
                corr_name = rname
                dis = ndis
    if dis == 0:
        pass
    elif dis <= (len(name) // 3):
        logger.info(f"Corrected type from [{name}] to [{corr_name}] with distance {dis}")
    else:
        logger.warning(f"Corrected type from [{name}] to [{corr_name}] with distance {dis}")
    return corr_name


def type_auto_correct_EN(name: str) -> str:
    corr_name = ""
    dis = 10000000
    for arts in ArtsInfo.TypeNames_EN:
        for rname in arts:
            ndis = Levenshtein.distance(name, rname)
            if ndis < dis:
                corr_name = rname
                dis = ndis
    if dis == 0:
        pass
    elif dis <= (len(name) // 3):
        logger.info(f"Corrected type from [{name}] to [{corr_name}] with distance {dis}")
    else:
        logger.warning(f"Corrected type from [{name}] to [{corr_name}] with distance {dis}")
    return corr_name