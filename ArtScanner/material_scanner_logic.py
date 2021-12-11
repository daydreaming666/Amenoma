import time

import art_scanner_logic
import mouse
from utils import captureWindow
from typing import Tuple


class MaterialScannerLogic:
    def __init__(self, game_info: art_scanner_logic.GameInfo):
        self.scanner = art_scanner_logic.ArtScannerLogic(game_info)

    def interrupt(self):
        self.scanner.interrupt()

    # def waitSwitched(self, art_center_x, art_center_y, min_wait=0.1, max_wait=3,
    #                  condition=lambda pix: sum(pix) / 3 > 200):
    #     self.scanner.waitSwitched(art_center_x, art_center_y, min_wait, max_wait,
    #                               condition)

    def getItemCenter(self, row: int, col: int):
        return self.scanner.getArtCenter(row, col)

    def scanMora(self):
        """scan Mora and Primogems"""
        pass

    def clickCDIButton(self):
        """click Character Development Items button"""
        mouse.move(*self.scanner.game_info.cdi_button)
        mouse.click()
        time.sleep(0.5)

    def clickMaterialButton(self):
        """click Material button"""
        mouse.move(*self.scanner.game_info.m_button)
        mouse.click()
        time.sleep(0.5)

    def scanRows(self, rows, callback) -> bool:
        def getItemCoord(row: int, col: int, lastrow=False) -> Tuple[int, int, int, int]:
            """
            get the coord of the item
            :param row:
            :param col:
            :param lastrow:
            :return: (x1, y1, x2, y2): Tuple[int, int, int, int]
            """
            g = self.scanner.game_info
            x1 = int(g.first_art_x + (g.art_width + g.art_gap_x) * col)
            y1 = int(g.first_art_y + (g.art_height + g.art_gap_y) * row)
            x2 = int(g.first_art_x + (g.art_width + g.art_gap_x) * col + g.art_width)
            y2 = int(g.first_art_y + (g.art_height + g.art_gap_y) * row + g.art_height)

            if lastrow:
                y1 -= g.lastrow_offset
                y2 -= g.lastrow_offset

            return x1, y1, x2, y2

        last_row = rows[0] != 0
        rows = list(rows)
        if len(rows) < 1:
            return True
        art_center_x, art_center_y = self.getItemCenter(rows[0], 0)
        mouse.move(self.scanner.game_info.left + art_center_x, self.scanner.game_info.top + art_center_y)
        mouse.click()

        if last_row:
            time.sleep(0.5)
        for art_row in rows:
            for art_col in range(self.scanner.game_info.art_cols):
                if self.scanner.stopped:
                    return False

                if self.scanner.waitSwitched(art_center_x, art_center_y, min_wait=0.1, max_wait=3):
                    detail_img = captureWindow(self.scanner.game_info.hwnd, (
                        self.scanner.game_info.art_info_left,
                        self.scanner.game_info.art_info_top,
                        self.scanner.game_info.art_info_left + self.scanner.game_info.art_info_width,
                        self.scanner.game_info.art_info_top + self.scanner.game_info.art_info_height))
                    item_img = captureWindow(self.scanner.game_info.hwnd,
                                             getItemCoord(art_row, art_col, last_row))
                    if art_col == self.scanner.game_info.art_cols - 1:
                        art_row += 1
                        art_col = 0
                    else:
                        art_col += 1
                    if art_row in rows:
                        art_center_x, art_center_y = self.getItemCenter(art_row, art_col)
                        mouse.move(self.scanner.game_info.left + art_center_x,
                                   self.scanner.game_info.top + art_center_y)
                        mouse.click()
                    callback(detail_img, item_img)
                else:
                    return False
        return True

    def is_between_rows(self) -> bool:
        pix = captureWindow(self.scanner.game_info.hwnd, (
                self.scanner.game_info.scroll_fin_keypt_x,
                self.scanner.game_info.scroll_fin_keypt_y,
                self.scanner.game_info.scroll_fin_keypt_x + 1.5,
                self.scanner.game_info.scroll_fin_keypt_y + 1.5))

        return any(abs(p1 - p2) > 5 for p1, p2 in zip(pix.getpixel((0, 0)), (233, 229, 220)))

    def alignFirstRow(self):
        return self.scanner.alignFirstRow()

    def scrollToRow(self, target_row, max_scrolls=20, extra_scroll=0, interval=0.05) -> int:
        return self.scanner.scrollToRow(target_row - 1, max_scrolls, extra_scroll, interval)
