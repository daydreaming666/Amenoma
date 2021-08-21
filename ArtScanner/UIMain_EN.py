import ctypes
import json
import os
import sys
import time

import mouse
from PyQt5.Qt import QThread
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QProgressBar

import ocr_EN
from UIWindow_EN import Ui_MainWindow
from art_saver_EN import ArtDatabase
from art_scanner_logic import ArtScannerLogic, GameInfo
from utils import decodeValue, findWindowsByName, setWindowToForeground

window_name_cn = '原神'
window_name_en = 'Genshin Impact'

window_name = window_name_en

if len(sys.argv) > 1:
    bundle_dir = sys.argv[1]
else:
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))


def isAdmin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


class UIMain(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(UIMain, self).__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.pushButton_click)
        self.pushButton_2.clicked.connect(self.pushButton2_click)
        self.hwnd_get = False
        self.initEngine()

    def initEngine(self):
        self.print_log("Initializing... please wait...")
        if not isAdmin():
            msgbox = QMessageBox.warning(self, 'Error', 'Please select Run as administrator in the right-click menu ', QMessageBox.Yes, QMessageBox.Yes)
            sys.exit(0)
        self.initDpi()
        self.print_log("Initialization is complete! ")

    class ProgressBarThread(QThread):
        def __init__(self, bar: QProgressBar):
            self.bar = bar
            super().__init__()

        def run(self) -> None:
            while self.bar.value() < 100:
                self.bar.setValue(self.bar.value() + 1)
                time.sleep(0.1)

    # 点击 「捕获窗口」
    def pushButton_click(self):
        self.progressBar.setValue(0)
        self.textBrowser_3.append("Catching window... please wait :)")
        pbThread = self.ProgressBarThread(self.progressBar)
        pbThread.run()

        while True:
            windows = findWindowsByName(window_name)

            if len(windows) == 0:
                self.textBrowser_3.append("No running Genshin Impact found, please try to capture again ")
            elif len(windows) == 1:
                self.hwnd = windows[0][0]
                break
            else:
                self.textBrowser_3.append(f"Found multiple windows named {window_name}, please try to capture again")

        self.progressBar.setValue(100)
        self.game_info = GameInfo(self.hwnd)

        if self.game_info.w == 0 or self.game_info.h == 0:
            self.textBrowser_3.append(f"Not support full screen mode, , please try to capture again")
            self.hwnd_get = False
        else:
            self.hwnd_get = True
            self.textBrowser_3.append(f"Successful, start scanning now!")
            self.game_info.calculateCoordinates()

    # 点击「开始扫描」
    def pushButton2_click(self):
        QMessageBox.information(self, "info", "Please open Bag - Artifacts and turn to the top of list ", QMessageBox.Ok, QMessageBox.Ok)
        QApplication.processEvents()
        self.print_log("Initialize the OCR model ...")
        self.ocr_model = ocr_EN.OCR(scale_ratio=self.game_info.scale_ratio,
                                 model_weight=os.path.join(bundle_dir, 'weights-improvement-EN-81-1.00.hdf5'))

        QApplication.processEvents()
        self.print_log("Initialize data...")
        self.art_id = 0
        self.saved = 0
        self.skipped = 0
        self.failed = 0
        self.star_dist = [0, 0, 0, 0, 0]
        self.star_dist_saved = [0, 0, 0, 0, 0]

        QApplication.processEvents()
        self.print_log("Creating folder ...")
        os.makedirs('artifacts_EN', exist_ok=True)

        QApplication.processEvents()
        if self.game_info.incomplete_lastrow:
            self.print_log(
                f'Detected that the Bag has {self.game_info.art_rows} rows {self.game_info.art_cols} columns,'
                f'but the incomplete last line may affect the effect of automatic page turning, '
                f'It is recommended to change the resolution to 16:9')
        else:
            self.print_log(f'Detected that the Bag has {self.game_info.art_rows} rows '
                           f'{self.game_info.art_cols} columns, make sure it is correct.')

        QApplication.processEvents()

        time.sleep(2)

        QApplication.processEvents()
        self.export_type = self.comboBox.currentIndex()
        self.print_log(f'Export format = {self.comboBox.currentText()}')

        self.level_threshold = self.spinBox.value()
        self.print_log(f'Level threshold = {self.level_threshold}')

        self.rarity_threshold = self.spinBox_2.value()
        self.print_log(f'Star threshold = {self.rarity_threshold}')

        self.scroll_interval = self.doubleSpinBox.value()
        self.print_log(f'Detection delay = {self.scroll_interval}')

        QApplication.processEvents()
        self.print_log('The program will start running automatically ')
        self.print_log('Please keep the Genshin Impact in the foreground during running, '
                       'do not block the window or using the mouse, '
                       'press the middle mouse button to stop. ')

        QApplication.processEvents()
        self.print_log('8...')
        time.sleep(1)
        QApplication.processEvents()
        self.print_log('7...')
        time.sleep(1)
        QApplication.processEvents()
        self.print_log('6...')
        time.sleep(1)

        QApplication.processEvents()
        self.print_log('OCR will start running in 5 seconds,'
                       ' if this prompt does not automatically switch to the original window,'
                       ' please manually click the original window to switch to the foreground.')
        QApplication.processEvents()
        setWindowToForeground(self.hwnd)
        QApplication.processEvents()
        time.sleep(5)

        QApplication.processEvents()
        self.art_scanner = ArtScannerLogic(self.game_info)
        self.art_data = ArtDatabase('artifacts.dat')

        self.exporter = [self.art_data.exportGenshinArtJSON, self.art_data.exportMingyuLabJSON][int(self.export_type)]
        self.export_name = ['artifacts.genshinart.json', 'artifacts.mingyulab.json'][int(self.export_type)]
        mouse.on_middle_click(self.art_scanner.interrupt)

        QApplication.processEvents()
        self.print_log('Aligning')
        self.art_scanner.alignFirstRow()
        self.print_log('Align complete，Scanning now...')
        time.sleep(0.5)
        self.start_row = 0

        QApplication.processEvents()
        try:
            while True:
                QApplication.processEvents()
                if self.art_scanner.stopped or not self.art_scanner.scanRows(
                        rows=range(self.start_row, self.game_info.art_rows),
                        callback=self.artscannerCallback) or self.start_row != 0:
                    break
                self.start_row = self.game_info.art_rows - self.art_scanner.scrollToRow(self.game_info.art_rows,
                                                                                        max_scrolls=20,
                                                                                        extra_scroll=int(
                                                                                            self.game_info.art_rows > 5),
                                                                                        interval=self.scroll_interval)
                if self.start_row == self.game_info.art_rows:
                    break
            if self.art_scanner.stopped:
                self.print_log("User interrupted scanning.")
            elif self.start_row != 0:
                self.print_log("No next page, terminate.")
            else:
                self.print_log("No Artifact remained，terminate.")
        except Exception as e:
            self.print_log(f"Because of\"{repr(e)}\" stopped unexpectedly, "
                           f"Information Scanned will be saved.")

        if self.saved != 0:
            self.exporter(self.export_name)
        self.print_log(f'{self.skipped + self.saved}/{self.art_id} Scanned Artifacts total,'
                       f'{self.saved} Saved to {self.export_name}， {self.failed} failed')
        self.print_log('Invalid recognition / fails View in folder artifacts_EN')
        self.print_log('----------------------------')
        self.print_log('Star distribution ：(Saved / Scanned)')
        self.print_log(f'5: {self.star_dist_saved[4]}/{self.star_dist[4]}')
        self.print_log(f'4: {self.star_dist_saved[3]}/{self.star_dist[3]}')
        self.print_log(f'3: {self.star_dist_saved[2]}/{self.star_dist[2]}')
        self.print_log(f'2: {self.star_dist_saved[1]}/{self.star_dist[1]}')
        self.print_log(f'1: {self.star_dist_saved[0]}/{self.star_dist[0]}')
        self.print_log('----------------------------')
        self.print_log('Completed!')

    def artscannerCallback(self, art_img):
        QApplication.processEvents()
        info = self.ocr_model.detect_info(art_img)
        self.star_dist[info['star'] - 1] += 1
        if decodeValue(info['level']) < self.level_threshold or decodeValue(info['star']) < self.rarity_threshold:
            self.skipped += 1
        # todo dont raise error
        elif self.art_data.add(info, art_img, raise_error=True):
            self.saved += 1
            self.star_dist_saved[info['star'] - 1] += 1
        else:
            art_img.save(f'artifacts_EN/{self.art_id}.png')
            s = json.dumps(info, ensure_ascii=False)
            with open(f"artifacts_EN/{self.art_id}.json", "wb") as f:
                f.write(s.encode('utf-8'))
            self.failed += 1
        self.art_id += 1
        self.print_log(
            f"\r{self.art_id} Scanned, {self.saved} Saved, {self.skipped} Skipped")

    def print_log(self, text):
        self.textBrowser_4.append(text)

    def initDpi(self):
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
                self.print_log('It is detected that the process DPI setting is not supported '
                               '(maybe the system version is lower than Win10)')
                self.print_log('The program will continue to execute, '
                               'but there may be resolution issues on high-resolution screens.')
            except:
                self.print_log('It is detected that reading the system DPI setting is not supported'
                               ' (maybe the system version is lower than Win8) ')
                self.print_log('The program will continue to execute, '
                               'but there may be resolution issues on high-resolution screens.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    uiMain = UIMain()
    uiMain.show()
    sys.exit(app.exec_())
