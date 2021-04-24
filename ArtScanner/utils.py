from mss import mss
from PIL import Image 
import win32gui

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
    return captureRect([screen_rect[1], screen_rect[0], screen_rect[2]-screen_rect[0], screen_rect[3]-screen_rect[1]])

def decodeValue(v):
    if type(v)!=str:
        return v
    if "%" in v:
        return float(v[:-1])/100
    else:
        return int(v.replace(',', '').replace('+', ''))