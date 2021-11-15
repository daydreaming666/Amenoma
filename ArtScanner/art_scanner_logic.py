import math
import time
from typing import Tuple

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


class ArtScannerLogic:
    def __init__(self, game_info: GameInfo):
        self.game_info = game_info
        self.stopped = False
        self.avg_response_time = 1 / 60

    def interrupt(self):
        self.stopped = True

    def waitSwitched(self, art_center_x, art_center_y, min_wait=0.1, max_wait=3,
                     condition=lambda pix: sum(pix) / 3 > 200):
        start = time.time()
        mouse.move(self.game_info.left + art_center_x, self.game_info.top + art_center_y)
        for _ in range(math.ceil(max_wait / min_wait)):
            mouse.click()
            pix = captureWindow(self.game_info.hwnd, (
                art_center_x - self.game_info.art_width / 2 - self.game_info.art_expand,
                art_center_y,
                art_center_x - self.game_info.art_width / 2 - self.game_info.art_expand + 1.5,
                art_center_y + 1.5))

            if condition(pix.getpixel((0, 0))):
                self.avg_response_time = 0.5 * (self.avg_response_time + time.time() - start)
                return True

            time.sleep(min_wait)

        return False

    def getArtCenter(self, row: int, col: int) -> Tuple[float, float]:
        """
        :param row: represents the row in the items grid
        :param col: represents the col in the items grid
        :return: xy coordinate of item's icon center in
        """
        gi = self.game_info
        x = gi.first_art_x + (gi.art_width + gi.art_gap_x) * col + gi.art_width / 2
        y = gi.first_art_y + (gi.art_height + gi.art_gap_y) * row + gi.art_height / 5
        return x, y

    def scanRows(self, rows, callback):
        for art_row in rows:
            for art_col in range(self.game_info.art_cols):
                if self.stopped:
                    return False

                art_center_x, art_center_y = self.getArtCenter(art_row, art_col)
                if not self.waitSwitched(art_center_x, art_center_y, min_wait=0.1, max_wait=3):
                    return False

                art_img = captureWindow(self.game_info.hwnd, (
                    self.game_info.art_info_left,
                    self.game_info.art_info_top,
                    self.game_info.art_info_left + self.game_info.art_info_width,
                    self.game_info.art_info_top + self.game_info.art_info_height))

                callback(art_img)
        return True

    def is_between_rows(self) -> bool:
        pix = captureWindow(self.game_info.hwnd, (
            self.game_info.scroll_fin_keypt_x,
            self.game_info.scroll_fin_keypt_y,
            self.game_info.scroll_fin_keypt_x + 1.5,
            self.game_info.scroll_fin_keypt_y + 1.5))

        return any(abs(p1 - p2) > 5 for p1, p2 in zip(pix.getpixel((0, 0)), (233, 229, 220)))

    def alignFirstRow(self):
        if self.is_between_rows():
            mouse.wheel(3)
            time.sleep(0.1)
            self.scrollToRow(0)

    def scrollToRow(self, target_row, max_scrolls=20, extra_scroll=0, interval=0.05):
        in_between_row = False
        rows_scrolled = 0
        lines_scrolled = 0
        while True:
            if self.is_between_rows():
                in_between_row = True
            elif in_between_row:
                in_between_row = False
                rows_scrolled += 1
                lines_scrolled = 0
                # print(f'已翻{rows_scrolled}行')
                if rows_scrolled >= target_row:
                    mouse.wheel(-extra_scroll)
                    return rows_scrolled

            if lines_scrolled > max_scrolls:
                return rows_scrolled

            def get_first_art():
                return np.array(captureWindow(self.game_info.hwnd, (
                    self.game_info.first_art_x + self.game_info.art_width / 2 - 1,
                    self.game_info.first_art_y + self.game_info.art_height / 2,
                    self.game_info.first_art_x + self.game_info.art_width / 2 + 1,
                    self.game_info.first_art_y + self.game_info.art_height
                )))

            first_art = get_first_art()

            lines_to_scroll = 7 if lines_scrolled == 0 and target_row > 0 else 1
            mouse.wheel(-lines_to_scroll)
            lines_scrolled += lines_to_scroll

            time.sleep(self.avg_response_time)
            total_waited = 0
            while total_waited <= 5 and np.max(np.abs(get_first_art() - first_art)) <= 5:
                time.sleep(interval)
                total_waited += interval
