import math
import time

import mouse
import numpy as np
import win32gui

from utils import captureWindow


class GameInfo:
    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.w, self.h = win32gui.GetClientRect(self.hwnd)[2:]
        self.left, self.top = win32gui.ClientToScreen(self.hwnd, (0, 0))

    def calculateCoordinates(self):
        self.scale_ratio = min(self.w / 2560, self.h / 1440)

        self.art_width = 164.39 * self.scale_ratio
        self.art_height = 203.21 * self.scale_ratio
        self.art_expand = 6 * self.scale_ratio

        self.art_gap_x = 30.89 * self.scale_ratio
        self.art_gap_y = 30.35 * self.scale_ratio

        self.art_info_width = 656 * self.scale_ratio
        self.art_info_height = 1119 * self.scale_ratio

        self.left_margin = (199.33 if self.w < 2 * self.h else 295.33) * self.scale_ratio
        self.right_margin = (871.33 if self.w < 2 * self.h else 967.33) * self.scale_ratio
        self.info_margin = 0 if self.w < 2 * self.h else 96 * self.scale_ratio

        self.art_cols = int(math.floor(
            (self.w - self.left_margin - self.right_margin + self.art_gap_x) /
            (self.art_width + self.art_gap_x)))

        self.art_shift = ((self.w - self.left_margin - self.right_margin + self.art_gap_x)
                          - self.art_cols * (self.art_width + self.art_gap_x)) / 2

        self.first_art_x = self.left_margin + self.art_shift
        self.first_art_y = 161 * self.scale_ratio

        self.art_info_top = 160 * self.scale_ratio
        self.art_info_left = self.w - 837 * self.scale_ratio - self.info_margin
        # scroll_keypt_x = left_margin + art_shift + 158*scale_ratio
        # scroll_keypt_y = 1270*scale_ratio+h-1440*scale_ratio
        self.scroll_fin_keypt_x = self.left_margin + self.art_shift + 10 * self.scale_ratio
        self.scroll_fin_keypt_y = 335 * self.scale_ratio

        self.art_rows = round((1270 * self.scale_ratio + self.h - 1440 * self.scale_ratio
                               - self.first_art_y + self.art_gap_y) /
                              (self.art_height + self.art_gap_y))
        self.incomplete_lastrow = ((1270 * self.scale_ratio + self.h
                                    - 1440 * self.scale_ratio
                                    - self.first_art_y + self.art_gap_y) /
                                   (self.art_height + self.art_gap_y) - self.art_rows + 1) < 0.7

        self.lastrow_offset = 34.5 * self.scale_ratio
        # Character Development Item
        self.cdi_button = (self.left + 1025 * self.scale_ratio,
                           self.top + 70 * self.scale_ratio)
        # Materials
        self.m_button = (self.left + 1270 * self.scale_ratio,
                           self.top + 70 * self.scale_ratio)

class ArtScannerLogic:
    def __init__(self, game_info):
        self.game_info = game_info
        self.stopped = False
        self.avg_response_time = 1 / 60

    def interrupt(self):
        self.stopped = True

    def waitSwitched(self, art_center_x, art_center_y, min_wait=0.1, max_wait=3,
                     condition=lambda pix: sum(pix) / 3 > 200):
        start = time.time()
        total_wait = 0
        while True:
            mouse.move(self.game_info.left + art_center_x, self.game_info.top + art_center_y)
            mouse.click()
            pix = captureWindow(self.game_info.hwnd, (
                art_center_x - self.game_info.art_width / 2 - self.game_info.art_expand,
                art_center_y,
                art_center_x - self.game_info.art_width / 2 - self.game_info.art_expand + 1.5,
                art_center_y + 1.5))
            if condition(pix.getpixel((0, 0))):
                self.avg_response_time = 0.5 * self.avg_response_time + 0.5 * (time.time() - start)
                return True
            else:
                time.sleep(min_wait)
                total_wait += min_wait
            if total_wait > max_wait:
                return False

    def getArtCenter(self, row, col):
        art_center_x = self.game_info.first_art_x + (
                self.game_info.art_width + self.game_info.art_gap_x) * col + self.game_info.art_width / 2
        art_center_y = self.game_info.first_art_y + (
                self.game_info.art_height + self.game_info.art_gap_y) * row + self.game_info.art_height / 5
        return art_center_x, art_center_y

    def scanRows(self, rows, callback):
        '''
        callback: function to take in artifact image and do what ever you want
        '''
        rows = list(rows)
        if len(rows) < 1:
            return True
        art_center_x, art_center_y = self.getArtCenter(rows[0], 0)
        mouse.move(self.game_info.left + art_center_x, self.game_info.top + art_center_y)
        mouse.click()
        for art_row in rows:
            for art_col in range(self.game_info.art_cols):
                if self.stopped:
                    return False
                if self.waitSwitched(art_center_x, art_center_y, min_wait=0.1, max_wait=3):
                    art_img = captureWindow(self.game_info.hwnd, (
                        self.game_info.art_info_left,
                        self.game_info.art_info_top,
                        self.game_info.art_info_left + self.game_info.art_info_width,
                        self.game_info.art_info_top + self.game_info.art_info_height))
                    if art_col == self.game_info.art_cols - 1:
                        art_row += 1
                        art_col = 0
                    else:
                        art_col += 1
                    if art_row in rows:
                        art_center_x, art_center_y = self.getArtCenter(art_row, art_col)
                        mouse.move(self.game_info.left + art_center_x, self.game_info.top + art_center_y)
                        mouse.click()
                    callback(art_img)
                else:
                    return False
        return True

    def alignFirstRow(self):
        mouse.move(self.game_info.left + self.game_info.first_art_x, self.game_info.top + self.game_info.first_art_y)
        mouse.click()
        pix = captureWindow(self.game_info.hwnd, (
            self.game_info.scroll_fin_keypt_x,
            self.game_info.scroll_fin_keypt_y,
            self.game_info.scroll_fin_keypt_x + 1.5,
            self.game_info.scroll_fin_keypt_y + 1.5))
        if abs(pix.getpixel((0, 0))[0] - 233) > 5 or abs(pix.getpixel((0, 0))[1] - 229) > 5 or abs(
                pix.getpixel((0, 0))[2] - 220) > 5:
            for _ in range(3):
                mouse.wheel(1)
            time.sleep(0.1)
            self.scrollToRow(0)

    def scrollToRow(self, target_row, max_scrolls=20, extra_scroll=0, interval=0.05):
        in_between_row = False
        rows_scrolled = 0
        lines_scrolled = 0
        while True:
            pix = captureWindow(self.game_info.hwnd, (
                self.game_info.scroll_fin_keypt_x,
                self.game_info.scroll_fin_keypt_y,
                self.game_info.scroll_fin_keypt_x + 1.5,
                self.game_info.scroll_fin_keypt_y + 1.5))
            if abs(pix.getpixel((0, 0))[0] - 233) > 5 or abs(pix.getpixel((0, 0))[1] - 229) > 5 or abs(
                    pix.getpixel((0, 0))[2] - 220) > 5:
                # if in_between_row==False:
                #     print('到行之间了')
                in_between_row = True
            elif in_between_row:
                in_between_row = False
                rows_scrolled += 1
                lines_scrolled = 0
                # print(f'已翻{rows_scrolled}行')
                if rows_scrolled >= target_row:
                    for _ in range(extra_scroll):
                        mouse.wheel(-1)
                    return rows_scrolled
            if lines_scrolled > max_scrolls:
                return rows_scrolled
            get_first_art = lambda: np.array(captureWindow(self.game_info.hwnd, (
                self.game_info.first_art_x + self.game_info.art_width / 2 - 1,
                self.game_info.first_art_y + self.game_info.art_height / 2,
                self.game_info.first_art_x + self.game_info.art_width / 2 + 1,
                self.game_info.first_art_y + self.game_info.art_height)))
            first_art = get_first_art()
            for _ in range(7 if lines_scrolled == 0 and target_row > 0 else 1):
                mouse.wheel(-1)
                lines_scrolled += 1
                # print('翻一下')
            time.sleep(self.avg_response_time)
            total_waited = 0
            while True:
                if total_waited > 5:
                    break
                if np.max(np.abs(get_first_art() - first_art)) > 5:
                    break
                time.sleep(interval)
                total_waited += interval
