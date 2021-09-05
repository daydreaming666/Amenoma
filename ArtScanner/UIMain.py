import ctypes
import json
import os
import sys
import time

import mouse
import win32api
import win32gui
from PyQt5.QtCore import (pyqtSignal, pyqtSlot, QObject, QThread,
                          QMutex, QWaitCondition)
from PyQt5.QtGui import (QMovie, QPixmap)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QDialog)

import ocr
import utils
from art_saver import ArtDatabase
from art_scanner_logic import ArtScannerLogic, GameInfo
from rcc import About_Dialog
from rcc import Help_Dialog
from rcc.MainWindow import Ui_MainWindow


class AboutDlg(QDialog, About_Dialog.Ui_Dialog):
    def __init__(self, parent=None):
        super(AboutDlg, self).__init__(parent)
        self.setupUi(self)


class HelpDlg(QDialog, Help_Dialog.Ui_Dialog):
    def __init__(self, parent=None):
        super(HelpDlg, self).__init__(parent)
        self.setupUi(self)


class UIMain(QMainWindow, Ui_MainWindow):
    captureWindowSignal = pyqtSignal()
    startScanSignal = pyqtSignal(dict)
    initializeSignal = pyqtSignal()
    detectGameInfoSignal = pyqtSignal()

    def __init__(self):
        super(UIMain, self).__init__()
        self.setupUi(self)

        self.exportFileName = ''
        self.gif = QMovie(':/rcc/rcc/loading.gif')
        self.picOk = QPixmap(':/rcc/rcc/ok.png')

        # 连接按钮
        self.pushButton.clicked.connect(self.startScan)
        self.pushButton_2.clicked.connect(self.captureWindow)
        self.pushButton_3.clicked.connect(self.showHelpDlg)
        self.pushButton_4.clicked.connect(self.showExportedFile)
        self.pushButton_5.clicked.connect(self.showExtraSettings)
        self.pushButton_6.clicked.connect(self.showAboutDlg)

        # 创建工作线程
        self.worker = Worker()
        self.workerThread = QThread()
        self.worker.moveToThread(self.workerThread)

        self.worker.printLog.connect(self.printLog)
        self.worker.printErr.connect(self.printErr)
        self.worker.working.connect(self.onWorking)
        self.worker.endWorking.connect(self.endWorking)
        self.worker.endInit.connect(self.endInit)
        self.worker.endScan.connect(self.endScan)

        self.initializeSignal.connect(self.worker.initEngine)
        self.detectGameInfoSignal.connect(self.worker.detectGameInfo)
        self.startScanSignal.connect(self.worker.scanArts)

        self.workerThread.start()

        self.initialize()

    # 通知工作线程进行初始化
    def initialize(self):
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.initializeSignal.emit()

    @pyqtSlot()
    def endInit(self):
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)

    @pyqtSlot()
    def onWorking(self):
        self.label.setMovie(self.gif)
        self.gif.start()

    @pyqtSlot()
    def endWorking(self):
        self.label.setPixmap(self.picOk)

    @pyqtSlot()
    def showHelpDlg(self):
        dlg = HelpDlg(self)
        point = self.rect().topRight()
        globalPoint = self.mapToGlobal(point)
        dlg.move(globalPoint)
        return dlg.show()

    @pyqtSlot()
    def showAboutDlg(self):
        dlg = AboutDlg(self)
        return dlg.show()

    @pyqtSlot()
    def showExtraSettings(self):
        pass

    @pyqtSlot(str)
    def printLog(self, log: str):
        self.textBrowser_3.append(log)
        QApplication.processEvents()

    @pyqtSlot(str)
    def printErr(self, err: str):
        self.textBrowser_3.append(f'<font color="red">{err}</font>')

    @pyqtSlot()
    def captureWindow(self):
        self.detectGameInfoSignal.emit()

    @pyqtSlot()
    def startScan(self):
        info = {
            "star": [self.checkBox_5.isChecked(),
                     self.checkBox_4.isChecked(),
                     self.checkBox_3.isChecked(),
                     self.checkBox_2.isChecked(),
                     self.checkBox.isChecked()],
            "levelMin": self.spinBox.value(),
            "levelMax": self.spinBox_2.value(),
            "delay": self.doubleSpinBox.value(),
            "exporter": (0 if self.radioButton.isChecked() else
                         1 if self.radioButton_2.isChecked() else
                         2 if self.radioButton_3.isChecked() else -1)
        }

        self.setUIEnabled(False)

        self.startScanSignal.emit(info)

    def setUIEnabled(self, e: bool):
        self.pushButton.setEnabled(e)
        self.checkBox.setEnabled(e)
        self.checkBox_2.setEnabled(e)
        self.checkBox_3.setEnabled(e)
        self.checkBox_4.setEnabled(e)
        self.checkBox_5.setEnabled(e)

        self.spinBox.setEnabled(e)
        self.spinBox_2.setEnabled(e)
        self.doubleSpinBox.setEnabled(e)

        self.radioButton.setEnabled(e)
        self.radioButton_2.setEnabled(e)
        self.radioButton_3.setEnabled(e)

    @pyqtSlot(str)
    def endScan(self, filename: str):
        self.setUIEnabled(True)
        self.exportFileName = filename

    @pyqtSlot()
    def showExportedFile(self):
        if self.exportFileName != '':
            s = "/select, " + os.path.abspath(self.exportFileName)
            win32api.ShellExecute(None, "open", "explorer.exe", s, None, 1)
        else:
            self.printErr("无导出文件")


class Worker(QObject):
    printLog = pyqtSignal(str)
    printErr = pyqtSignal(str)
    working = pyqtSignal()
    endWorking = pyqtSignal()
    endInit = pyqtSignal()
    endScan = pyqtSignal(str)

    def __init__(self):
        super(Worker, self).__init__()
        self.isQuit = False
        self.workingMutex = QMutex()
        self.cond = QWaitCondition()
        self.isInitialized = False
        self.isWindowCaptured = False

        # in initEngine
        self.game_info = None
        self.model = None
        self.bundle_dir = None

        # init in scanArts
        self.art_id = 0
        self.saved = 0
        self.skipped = 0
        self.failed = 0
        self.star_dist = [0, 0, 0, 0, 0]
        self.star_dist_saved = [0, 0, 0, 0, 0]
        self.detectSettings = None

    @pyqtSlot()
    def initEngine(self):
        self.working.emit()

        # yield the thread
        time.sleep(0.5)
        self.log('初始化中，请稍候...')

        # 创建文件夹
        os.makedirs('artifacts', exist_ok=True)
        self.log('检测 DPI 设定...')
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
                self.error('检测到不支持进程 DPI 设置（可能是系统版本低于 Win10）')
                self.error('程序将会继续，但可能存在分辨率问题')
            except:
                self.error('检测到不支持读取系统 DPI 设置（可能是系统版本低于 Win8）')
                self.error('程序将会继续，但可能存在分辨率问题')

        self.log('尝试捕获窗口...')
        self.endworking.emit()

        self.detectGameInfo()

        self.working.emit()
        self.log('初始化 OCR 模型...')
        if len(sys.argv) > 1:
            self.bundle_dir = sys.argv[1]
        else:
            self.bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

        self.model = ocr.OCR(model_weight=os.path.join(self.bundle_dir, 'weights-improvement-55-1.00.hdf5'))

        self.log('初始化完成')
        if self.isWindowCaptured:
            self.log('窗口已捕获，请检查行列数正确后开始扫描')
            self.log(f'行: {self.game_info.art_rows} , 列: {self.game_info.art_cols}')
            self.log('错误请更换分辨率后重试')
        else:
            self.error('窗口未捕获，请在重新捕获窗口后开始扫描')

        self.log('开始扫描前请打开背包 - 圣遗物，并翻页至顶部')
        self.endWorking.emit()
        self.endInit.emit()

    # 捕获窗口与计算边界
    @pyqtSlot()
    def detectGameInfo(self):
        self.working.emit()
        hwnd = self.captureWindow()
        if self.isWindowCaptured:
            self.game_info = GameInfo(hwnd)
            if self.game_info.w == 0 or self.game_info.h == 0:
                self.isWindowCaptured = False
                self.error("当前原神窗口为全屏模式或最小化, 请调整后重新捕获窗口")
            else:
                self.game_info.calculateCoordinates()
        self.endWorking.emit()

    # 捕获窗口
    def captureWindow(self) -> int:
        hwnd = win32gui.FindWindow("UnityWndClass", "原神")
        if hwnd > 0:
            self.isWindowCaptured = True
            self.log('捕获窗口成功')
        else:
            self.isWindowCaptured = False
            self.error('捕获窗口失败')
        return hwnd

    @pyqtSlot(dict)
    def scanArts(self, info: dict):
        self.working.emit()
        if not self.isWindowCaptured:
            self.error('窗口未捕获，请重新捕获窗口')
            self.endScan.emit('')
            self.endWorking.emit()
            return

        self.model.setScaleRatio(self.game_info.scale_ratio)

        if info['levelMin'] > info['levelMax']:
            self.error('最小值与最大值设置有误')
            self.endScan.emit('')
            self.endWorking.emit()
            return
        self.detectSettings = info
        artifactDB = ArtDatabase()
        artScanner = ArtScannerLogic(self.game_info)

        exporter = [artifactDB.exportGenshinArtJSON,
                    artifactDB.exportMingyuLabJSON,
                    artifactDB.exportGenshinOptimizerJSON][info['exporter']]
        export_name = ['artifacts.genshinart.json',
                       'artifacts.mingyulab.json',
                       'artifacts.genshin-optimizer.json'][info['exporter']]

        mouse.on_middle_click(artScanner.interrupt)

        self.log('3 秒后将开始扫描...')
        time.sleep(1)
        utils.setWindowToForeground(self.game_info.hwnd)

        self.log('3...')
        time.sleep(1)
        self.log('2...')
        time.sleep(1)
        self.log('1...')
        time.sleep(1)

        self.log('自动对齐中...')
        artScanner.alignFirstRow()
        self.log('对齐完成，即将开始扫描')
        time.sleep(0.5)

        start_row = 0
        self.art_id = 0
        self.saved = 0
        self.skipped = 0
        self.failed = 0
        self.star_dist = [0, 0, 0, 0, 0]
        self.star_dist_saved = [0, 0, 0, 0, 0]

        def artscannerCallback(art_img):
            detectedInfo = self.model.detect_info(art_img)
            self.star_dist[detectedInfo['star'] - 1] += 1
            detectedLevel = utils.decodeValue(detectedInfo['level'])

            detectedStar = utils.decodeValue(detectedInfo['star'])

            if not ((self.detectSettings['levelMin'] <= detectedLevel <= self.detectSettings['levelMax']) and
                    (self.detectSettings['star'][detectedStar - 1])):
                self.skipped += 1
            elif artifactDB.add(detectedInfo, art_img):
                self.saved += 1
                self.star_dist_saved[detectedInfo['star'] - 1] += 1
            else:
                art_img.save(f'artifacts/fail_{self.art_id}.png')
                s = json.dumps(detectedInfo, ensure_ascii=False)
                with open(f"artifacts/fail_{self.art_id}.json", "wb") as f:
                    f.write(s.encode('utf-8'))
                self.failed += 1
            self.art_id += 1
            self.log(f"已扫描{self.art_id}个圣遗物，已保存{self.saved}个，已跳过{self.skipped}个")

        try:
            while True:
                if artScanner.stopped or not artScanner.scanRows(rows=range(start_row, self.game_info.art_rows),
                                                                 callback=artscannerCallback) or start_row != 0:
                    break
                start_row = self.game_info.art_rows - artScanner.scrollToRow(self.game_info.art_rows, max_scrolls=20,
                                                                             extra_scroll=int(
                                                                                 self.game_info.art_rows > 5),
                                                                             interval=self.detectSettings['delay'])
                if start_row == self.game_info.art_rows:
                    break
            if artScanner.stopped:
                self.log('扫描已中断')
            else:
                self.log('扫描已完成')
        except Exception as e:
            self.error(repr(e))
            self.log('扫描出错，已停止')

        if self.saved != 0:
            exporter(export_name)
        self.log(f'扫描: {self.saved}')
        self.log(f'  - 保存: {self.saved}')
        self.log(f'  - 跳过: {self.skipped}')
        self.log(f'失败: {self.failed}')
        self.log('失败结果已存储至 artifacts 文件夹')

        self.log('星级: (已保存 / 已扫描)')
        self.log(f'5: {self.star_dist_saved[4]} / {self.star_dist[4]}')
        self.log(f'4: {self.star_dist_saved[3]} / {self.star_dist[3]}')
        self.log(f'3: {self.star_dist_saved[2]} / {self.star_dist[2]}')
        self.log(f'2: {self.star_dist_saved[1]} / {self.star_dist[1]}')
        self.log(f'1: {self.star_dist_saved[0]} / {self.star_dist[0]}')

        del artifactDB
        self.endScan.emit(export_name)
        self.endWorking.emit()

    def log(self, content: str):
        self.printLog.emit(content)

    def error(self, err: str):
        self.printErr.emit(err)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    uiMain = UIMain()
    uiMain.show()
    app.exec()
