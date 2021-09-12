import ctypes
import json
import os
import sys
import time

import mouse
import win32api
import win32gui
from PyQt5.QtCore import (pyqtSignal, pyqtSlot, QObject, QThread,
                          QMutex, QWaitCondition, Qt)
from PyQt5.QtGui import (QMovie, QPixmap)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QDialog,
                             QWidget, QCheckBox, QHBoxLayout)

import ocr
import utils
import ArtsInfo
from art_saver import ArtDatabase
from art_scanner_logic import ArtScannerLogic, GameInfo
from rcc import About_Dialog
from rcc import Help_Dialog
from rcc import ExtraSettings_Dialog
from rcc import InputWindow_Dialog
from rcc.MainWindow import Ui_MainWindow


class AboutDlg(QDialog, About_Dialog.Ui_Dialog):
    def __init__(self, parent=None):
        super(AboutDlg, self).__init__(parent)
        self.setupUi(self)


class HelpDlg(QDialog, Help_Dialog.Ui_Dialog):
    def __init__(self, parent=None):
        super(HelpDlg, self).__init__(parent)
        self.setupUi(self)


class InputWindowDlg(QDialog, InputWindow_Dialog.Ui_Dialog):
    retVal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(InputWindowDlg, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.handleClick)

    @pyqtSlot()
    def handleClick(self):
        self.retVal.emit(self.lineEdit.text())


class ExtraSettingsDlg(QDialog, ExtraSettings_Dialog.Ui_Dialog):
    acceptSignal = pyqtSignal(dict)

    def _addCheckboxAt(self, row: int, col: int, state: bool, text: str = ""):
        checkBoxWidget = QWidget()
        checkBox = QCheckBox(text)
        layoutCheckbox = QHBoxLayout(checkBoxWidget)
        layoutCheckbox.addWidget(checkBox)
        layoutCheckbox.setAlignment(Qt.AlignLeft)
        layoutCheckbox.setContentsMargins(10, 0, 0, 0)

        if state:
            checkBox.setChecked(True)
        else:
            checkBox.setChecked(False)

        self._checkboxes.append(checkBox)
        self.tableWidget.setCellWidget(row, col, checkBoxWidget)

    def __init__(self, settings, parent=None):
        super(ExtraSettingsDlg, self).__init__(parent)
        self.setupUi(self)

        self._checkboxes = []

        self.checkBox.setChecked(settings['EnhancedCaptureWindow'])
        self.checkBox_2.setChecked(settings['ExportAllFormats'])
        self.checkBox_3.setChecked(settings['FilterArtsByName'])
        self.checkBox_4.setEnabled(settings['FilterArtsByName'])
        self.checkBox_5.setChecked(settings['ExportAllImages'])
        self.tableWidget.setEnabled(settings['FilterArtsByName'])

        self.checkBox_3.clicked.connect(self.handleAdvancedSettingsClicked)
        self.checkBox_4.clicked.connect(self.handleSelectAllClicked)
        self.pushButton.clicked.connect(self.handleAccept)

        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(len(ArtsInfo.SetNames))
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        for i, e in enumerate(ArtsInfo.SetNames):
            self._addCheckboxAt(i, 0, settings['Filter'][i], e)

    @pyqtSlot()
    def handleSelectAllClicked(self):
        if self.checkBox_4.isChecked():
            for e in self._checkboxes:
                e.setChecked(True)
        else:
            for e in self._checkboxes:
                e.setChecked(False)

    @pyqtSlot()
    def handleAdvancedSettingsClicked(self):
        if self.checkBox_3.isChecked():
            self.tableWidget.setEnabled(True)
            self.checkBox_4.setEnabled(True)
        else:
            self.tableWidget.setEnabled(False)
            self.checkBox_4.setEnabled(False)

    @pyqtSlot()
    def handleAccept(self):
        settings = {
            "EnhancedCaptureWindow": self.checkBox.isChecked(),
            "ExportAllFormats": self.checkBox_2.isChecked(),
            "ExportAllImages": self.checkBox_5.isChecked(),
            "FilterArtsByName": self.checkBox_3.isChecked(),
            "Filter": [i.isChecked() for i in self._checkboxes]
        }
        self.acceptSignal.emit(settings)


class UIMain(QMainWindow, Ui_MainWindow):
    startScanSignal = pyqtSignal(dict)
    initializeSignal = pyqtSignal()
    detectGameInfoSignal = pyqtSignal(bool)
    setWindowNameSignal = pyqtSignal(str)

    def __init__(self):
        super(UIMain, self).__init__()
        self.setupUi(self)

        self.exportFileName = ''
        self.gif = QMovie(':/rcc/rcc/loading.gif')
        self.picOk = QPixmap(':/rcc/rcc/ok.png')

        self._settings = {
            "EnhancedCaptureWindow": False,
            "ExportAllFormats": False,
            "ExportAllImages": False,
            "FilterArtsByName": False,
            "Filter": [True for _ in ArtsInfo.SetNames]
        }
        self._helpDlg = HelpDlg(self)
        self._isHelpDlgShowing = False

        # 连接按钮
        self.pushButton.clicked.connect(self.startScan)
        self.pushButton_2.clicked.connect(self.captureWindow)
        self.pushButton_3.clicked.connect(self.showHelpDlg)
        self.pushButton_4.clicked.connect(self.showExportedFile)
        self.pushButton_5.clicked.connect(self.showExtraSettings)
        self.pushButton_6.clicked.connect(self.showAboutDlg)

        self.radioButton.clicked.connect(self.selectedMona)
        self.radioButton_2.clicked.connect(self.selectedMingyu)
        self.radioButton_3.clicked.connect(self.selectedGO)

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
        self.worker.showInputWindow.connect(self.showInputWindowName)

        self.initializeSignal.connect(self.worker.initEngine)
        self.detectGameInfoSignal.connect(self.worker.detectGameInfo)
        self.startScanSignal.connect(self.worker.scanArts)
        self.setWindowNameSignal.connect(self.worker.setWindowName)

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
        point = self.rect().topRight()
        globalPoint = self.mapToGlobal(point)
        self._helpDlg.move(globalPoint)
        self._helpDlg.show()

    @pyqtSlot()
    def showAboutDlg(self):
        dlg = AboutDlg(self)
        dlg.exec()

    @pyqtSlot()
    def selectedMona(self):
        self.checkBox.setChecked(True)
        self.checkBox_2.setChecked(True)
        self.checkBox_3.setChecked(False)
        self.checkBox_4.setChecked(False)
        self.checkBox_5.setChecked(False)

        self.spinBox.setValue(0)
        self.spinBox_2.setValue(20)

    @pyqtSlot()
    def selectedMingyu(self):
        self.checkBox.setChecked(True)
        self.checkBox_2.setChecked(False)
        self.checkBox_3.setChecked(False)
        self.checkBox_4.setChecked(False)
        self.checkBox_5.setChecked(False)

        self.spinBox.setValue(4)
        self.spinBox_2.setValue(20)

    @pyqtSlot()
    def selectedGO(self):
        self.checkBox.setChecked(True)
        self.checkBox_2.setChecked(True)
        self.checkBox_3.setChecked(False)
        self.checkBox_4.setChecked(False)
        self.checkBox_5.setChecked(False)

        self.spinBox.setValue(0)
        self.spinBox_2.setValue(20)

    @pyqtSlot()
    def showExtraSettings(self):
        dlg = ExtraSettingsDlg(self._settings, self)
        dlg.acceptSignal.connect(self.handleExtraSettings)
        dlg.exec()

    @pyqtSlot(str, bool)
    def showInputWindowName(self, window_name: str, isDup: bool):
        dlg = InputWindowDlg(self)
        if not isDup:
            dlg.label.setText(f"未找到标题为 {window_name} 的窗口，请输入窗口标题后重新捕获")
        else:
            dlg.label.setText(f"找到多个标题为 {window_name} 的窗口，请输入窗口标题后重新捕获")
        dlg.retVal.connect(self.handleInputWindowRet)
        dlg.exec()

    @pyqtSlot(str)
    def handleInputWindowRet(self, window_name):
        self.setWindowNameSignal.emit(window_name)

    @pyqtSlot(str)
    def printLog(self, log: str):
        self.textBrowser_3.append(log)
        QApplication.processEvents()

    @pyqtSlot(str)
    def printErr(self, err: str):
        self.textBrowser_3.append(f'<font color="red">{err}</font>')

    @pyqtSlot()
    def captureWindow(self):
        self.detectGameInfoSignal.emit(self._settings['EnhancedCaptureWindow'])

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
                         2 if self.radioButton_3.isChecked() else -1),
            "ExtraSettings": self._settings
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

    @pyqtSlot(dict)
    def handleExtraSettings(self, ret: dict):
        self._settings = ret

        self.groupBox_4.setEnabled(self._settings['ExportAllFormats'])


class Worker(QObject):
    printLog = pyqtSignal(str)
    printErr = pyqtSignal(str)
    working = pyqtSignal()
    endWorking = pyqtSignal()
    endInit = pyqtSignal()
    endScan = pyqtSignal(str)
    showInputWindow = pyqtSignal(str, bool)

    def __init__(self):
        super(Worker, self).__init__()
        self.isQuit = False
        self.workingMutex = QMutex()
        self.cond = QWaitCondition()
        self.isInitialized = False
        self.isWindowCaptured = False

        self.windowName = '原神'
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

        self.endWorking.emit()

        self.detectGameInfo(False)

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
    @pyqtSlot(bool)
    def detectGameInfo(self, isEnhanced: bool):
        self.working.emit()
        if not isEnhanced:
            self.log('尝试捕获窗口...')
            hwnd = self.captureWindow()
        else:
            self.log(f'正在以增强模式捕获窗口 {self.windowName}...')
            hwnd = self.captureWindowEnhanced()
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

    @pyqtSlot(str)
    def setWindowName(self, name: str):
        self.windowName = name
        self.log(f'已将窗口名设为{name}, 请重新捕获')

    # 捕获窗口 强化版
    @pyqtSlot(str)
    def captureWindowEnhanced(self) -> int:
        hwnd = -1
        windows = utils.findWindowsByName(self.windowName)
        if len(windows) == 0:
            self.isWindowCaptured = False
            self.showInputWindow.emit(self.windowName, False)
        elif len(windows) == 1:
            self.isWindowCaptured = True
            hwnd = windows[0][0]
            self.log(f"以窗口名{self.windowName}捕获窗口成功")
        else:
            self.isWindowCaptured = False
            self.showInputWindow.emit(self.windowName, True)
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
                    artifactDB.exportGenmoCalcJSON,
                    artifactDB.exportGOODJSON]
        export_name = ['artifacts.genshinart.json',
                       'artifacts.genmocalc.json',
                       'artifacts.GOOD.json']

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

        def artFilter(detected_info, art_img):
            detected_info['name'] = utils.name_auto_correct(detected_info['name'])
            self.star_dist[detected_info['star'] - 1] += 1
            detectedLevel = utils.decodeValue(detected_info['level'])
            detectedStar = utils.decodeValue(detected_info['star'])

            if (self.detectSettings["ExtraSettings"]["FilterArtsByName"] and
                    (not self.detectSettings["ExtraSettings"]["Filter"][detected_info['name']])):
                self.skipped += 1
                status = 1
            elif not ((self.detectSettings['levelMin'] <= detectedLevel <= self.detectSettings['levelMax']) and
                      (self.detectSettings['star'][detectedStar - 1])):
                self.skipped += 1
                status = 1
            elif artifactDB.add(detected_info, art_img):
                self.saved += 1
                status = 2
                self.star_dist_saved[detected_info['star'] - 1] += 1
            else:
                status = 3
                self.failed += 1
            self.art_id += 1
            saveImg(detected_info, art_img, status)

        def saveImg(detected_info, art_img, status):
            if self.detectSettings['ExtraSettings']['ExportAllImages']:
                if status == 3:
                    art_img.save(f'artifacts/fail_{self.art_id}.png')
                    s = json.dumps(detected_info, ensure_ascii=False)
                    with open(f"artifacts/fail_{self.art_id}.json", "wb") as f:
                        f.write(s.encode('utf-8'))
                else:
                    art_img.save(f'artifacts/{self.art_id}.png')
                    s = json.dumps(detected_info, ensure_ascii=False)
                    with open(f"artifacts/{self.art_id}.json", "wb") as f:
                        f.write(s.encode('utf-8'))
            else:
                # export only failed
                if status == 3:
                    art_img.save(f'artifacts/fail_{self.art_id}.png')
                    s = json.dumps(detected_info, ensure_ascii=False)
                    with open(f"artifacts/fail_{self.art_id}.json", "wb") as f:
                        f.write(s.encode('utf-8'))

        def artscannerCallback(art_img):
            detectedInfo = self.model.detect_info(art_img)
            artFilter(detectedInfo, art_img)
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
            if info['ExtraSettings']['ExportAllFormats']:
                list(map(lambda exp, name: exp(name), exporter, export_name))
            else:
                self.log(f"导出文件: {export_name[info['exporter']]}")
                exporter[info['exporter']](export_name[info['exporter']])
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
        self.endScan.emit(export_name[info['exporter']])
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
