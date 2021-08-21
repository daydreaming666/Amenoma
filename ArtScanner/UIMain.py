import ctypes
import json
import os
import sys
import time

import mouse
from PyQt5.Qt import QThread
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QProgressBar

import ocr
from UIWindow import Ui_MainWindow
from art_saver import ArtDatabase
from art_scanner_logic import ArtScannerLogic, GameInfo
from utils import decodeValue, findWindowsByName, setWindowToForeground

window_name_cn = '原神'
window_name_en = 'Genshin Impact'

window_name = window_name_cn

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
        self.print_log("初始化中...请等待")
        if not isAdmin():
            msgbox = QMessageBox.warning(self, 'Error', '请在右键菜单选择以管理员身份运行', QMessageBox.Yes, QMessageBox.Yes)
            sys.exit(0)
        self.initDpi()
        self.print_log("初始化完成！")

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
        self.textBrowser_3.append("捕获窗口中...请等待")
        pbThread = self.ProgressBarThread(self.progressBar)
        pbThread.run()

        while True:
            windows = findWindowsByName(window_name)

            if len(windows) == 0:
                self.textBrowser_3.append("未找到在运行的原神, 请尝试重新捕获")
            elif len(windows) == 1:
                self.hwnd = windows[0][0]
                break
            else:
                self.textBrowser_3.append(f"发现多个窗口名为{window_name}, 请尝试重新捕获")

        self.progressBar.setValue(100)
        self.game_info = GameInfo(self.hwnd)

        if self.game_info.w == 0 or self.game_info.h == 0:
            self.textBrowser_3.append(f"不支持独占全屏模式, 请尝试重新捕获")
            self.hwnd_get = False
        else:
            self.hwnd_get = True
            self.textBrowser_3.append(f"捕获成功，请开始扫描")
            self.game_info.calculateCoordinates()

    # 点击「开始扫描」
    def pushButton2_click(self):
        QMessageBox.information(self, "info", "请打开圣遗物背包界面，翻到圣遗物列表顶部", QMessageBox.Ok, QMessageBox.Ok)
        QApplication.processEvents()
        self.print_log("初始化 OCR 模型...")
        self.ocr_model = ocr.OCR(scale_ratio=self.game_info.scale_ratio,
                                 model_weight=os.path.join(bundle_dir, 'weights-improvement-55-1.00.hdf5'))

        QApplication.processEvents()
        self.print_log("初始化数据...")
        self.art_id = 0
        self.saved = 0
        self.skipped = 0
        self.failed = 0
        self.star_dist = [0, 0, 0, 0, 0]
        self.star_dist_saved = [0, 0, 0, 0, 0]

        QApplication.processEvents()
        self.print_log("创建文件夹...")
        os.makedirs('artifacts', exist_ok=True)

        QApplication.processEvents()
        if self.game_info.incomplete_lastrow:
            self.print_log(
                f'检测到圣遗物背包有 {self.game_info.art_rows} 行 {self.game_info.art_cols} 列，但最后一行不完整可能会影响自动翻页效果，建议更改分辨率到16:9')
        else:
            self.print_log(f'检测到圣遗物背包有{self.game_info.art_rows} 行 {self.game_info.art_cols} 列，请务必确认是否正确！！错误请更改分辨率后重试')

        QApplication.processEvents()

        time.sleep(2)

        QApplication.processEvents()
        self.export_type = self.comboBox.currentIndex()
        self.print_log(f'导出格式 = {self.comboBox.currentText()}')

        self.level_threshold = self.spinBox.value()
        self.print_log(f'等级阈值 = {self.level_threshold}')

        self.rarity_threshold = self.spinBox_2.value()
        self.print_log(f'星级阈值 = {self.rarity_threshold}')

        self.scroll_interval = self.doubleSpinBox.value()
        self.print_log(f'检测延迟 = {self.scroll_interval}')

        QApplication.processEvents()
        self.print_log('程序即将自动开始运行')
        self.print_log('运行期间请保持原神在前台，请勿遮挡窗口或操作鼠标，按鼠标中键停止。')

        QApplication.processEvents()
        self.print_log('3...')
        time.sleep(1)
        QApplication.processEvents()
        self.print_log('2...')
        time.sleep(1)
        QApplication.processEvents()
        self.print_log('1...')
        time.sleep(1)

        QApplication.processEvents()
        self.print_log('OCR 将于 5 秒后开始运行,若此条提示显示时未自动切换到原神窗口，请手动点击原神窗口切到前台')
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
        self.print_log('正在自动对齐')
        self.art_scanner.alignFirstRow()
        self.print_log('对齐完成，即将开始扫描')
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
                self.print_log("用户已中断扫描")
            elif self.start_row != 0:
                self.print_log("没有检测到下一页圣遗物，自动终止")
            else:
                self.print_log("在最后点击位置未检测到圣遗物，自动终止")
        except Exception as e:
            self.print_log(f"因为\"{repr(e)}\"而意外停止扫描，将保存已扫描的圣遗物信息")

        if self.saved != 0:
            self.exporter(self.export_name)
        self.print_log(f'总计扫描了{self.skipped + self.saved}/{self.art_id}个圣遗物，'
                       f'保存了{self.saved}个到{self.export_name}，失败了{self.failed}个')
        self.print_log('无效识别/失败结果请到artifacts路径中查看')
        self.print_log('----------------------------')
        self.print_log('圣遗物星级分布：（保存数量/扫描数量）')
        self.print_log(f'5星：{self.star_dist_saved[4]}/{self.star_dist[4]}')
        self.print_log(f'4星：{self.star_dist_saved[3]}/{self.star_dist[3]}')
        self.print_log(f'3星：{self.star_dist_saved[2]}/{self.star_dist[2]}')
        self.print_log(f'2星：{self.star_dist_saved[1]}/{self.star_dist[1]}')
        self.print_log(f'1星：{self.star_dist_saved[0]}/{self.star_dist[0]}')
        self.print_log('----------------------------')
        self.print_log('已完成')

    def artscannerCallback(self, art_img):
        QApplication.processEvents()
        info = self.ocr_model.detect_info(art_img)
        self.star_dist[info['star'] - 1] += 1
        if decodeValue(info['level']) < self.level_threshold or decodeValue(info['star']) < self.rarity_threshold:
            self.skipped += 1
        elif self.art_data.add(info, art_img):
            self.saved += 1
            self.star_dist_saved[info['star'] - 1] += 1
        else:
            art_img.save(f'artifacts/{self.art_id}.png')
            s = json.dumps(info, ensure_ascii=False)
            with open(f"artifacts/{self.art_id}.json", "wb") as f:
                f.write(s.encode('utf-8'))
            self.failed += 1
        self.art_id += 1
        self.print_log(
            f"\r已扫描{self.art_id}个圣遗物，已保存{self.saved}个，已跳过{self.skipped}个")

    def print_log(self, text):
        self.textBrowser_4.append(text)

    def initDpi(self):
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
                self.print_log('检测到不支持进程DPI设置（可能是系统版本低于Win10）')
                self.print_log('程序将会继续执行，但在高分屏上可能存在分辨率问题')
            except:
                self.print_log('检测到不支持读取系统DPI设置（可能是系统版本低于Win8）')
                self.print_log('程序将会继续执行，但在高分屏上可能存在分辨率问题')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    uiMain = UIMain()
    uiMain.show()
    sys.exit(app.exec_())
