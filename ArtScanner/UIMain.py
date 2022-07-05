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
                             QWidget, QCheckBox, QHBoxLayout, QMessageBox)

import ArtsInfo
import ocr
import ocr_m
import utils
import config
import ToolboxMain

from art_saver import ArtDatabase
from art_scanner_logic import ArtScannerLogic, GameInfo
from material_saver import MaterialDatabase
from material_scanner_logic import MaterialScannerLogic
from rcc import About_Dialog
from rcc import ExtraSettings_Dialog
from rcc import Help_Dialog
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
        self.checkBox_6.setChecked(settings['ExportLocationField'])
        self.tableWidget.setEnabled(settings['FilterArtsByName'])
        self.tabWidget.setCurrentIndex(settings["TabIndex"])

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
            "ExportLocationField": self.checkBox_6.isChecked(),
            "Filter": [i.isChecked() for i in self._checkboxes],
            "TabIndex": self.tabWidget.currentIndex()
        }
        self.acceptSignal.emit(settings)


class UIMain(QMainWindow, Ui_MainWindow):
    startScanArtSignal = pyqtSignal(dict)
    startScanMaterialSignal = pyqtSignal(dict)
    initializeArtSignal = pyqtSignal()
    initializeMaterialSignal = pyqtSignal()
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
            "ExportLocationField": True,
            "Filter": [True for _ in ArtsInfo.SetNames],
            "TabIndex": 0
        }
        self._helpDlg = HelpDlg(self)
        self._toolbox = ToolboxMain.ToolboxUiMain()
        self._isHelpDlgShowing = False

        self.logger = utils.logger

        self._isArtScannerInitialized = False
        self._isMaterialScannerInitialized = False

        # connect the buttons
        # tab 1
        self.pushButton.clicked.connect(self.startScan)
        self.pushButton_2.clicked.connect(self.captureWindow)
        self.pushButton_5.clicked.connect(self.showExtraSettings)
        self.radioButton.clicked.connect(self.selectedMona)
        self.radioButton_2.clicked.connect(self.selectedGenmo)
        self.radioButton_3.clicked.connect(self.selectedGOOD)
        self.pushButton_9.clicked.connect(self.showToolbox)
        # bottom
        self.pushButton_3.clicked.connect(self.showHelpDlg)
        self.pushButton_4.clicked.connect(self.showExportedFile)
        self.pushButton_6.clicked.connect(self.showAboutDlg)
        # tab 2
        self.pushButton_7.clicked.connect(self.captureWindow)
        self.pushButton_8.clicked.connect(self.startScanMaterial)
        self.tabWidget.currentChanged.connect(self.handleTabChanged)
        self.checkBox_6.stateChanged.connect(self.handleScanOptions1Checked)
        self.checkBox_7.stateChanged.connect(self.handleScanOptions2Checked)

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

        self.initializeArtSignal.connect(self.worker.initArtEngine)
        self.initializeMaterialSignal.connect(self.worker.initMaterialEngine)
        self.detectGameInfoSignal.connect(self.worker.detectGameInfo)
        self.startScanArtSignal.connect(self.worker.scanArts)
        self.startScanMaterialSignal.connect(self.worker.scanMaterials)
        self.setWindowNameSignal.connect(self.worker.setWindowName)

        self.workerThread.start()

        self.initialize()

    # 通知工作线程进行初始化
    def initialize(self):
        self.logger.info("Worker thread initializing.")
        # tab 1
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        # tab 2
        self.pushButton_7.setEnabled(False)
        self.pushButton_8.setEnabled(False)
        self.initializeArtSignal.emit()

    @pyqtSlot(int)
    def handleScanOptions1Checked(self, state: int):
        """ Choose another when deselecting this
        Not allowed to choose neither """
        if state == 0 and not self.checkBox_7.isChecked():
            self.checkBox_7.setChecked(True)
            self.printLog("已选中「材料」")

    @pyqtSlot(int)
    def handleScanOptions2Checked(self, state: int):
        """Choose another when deselecting this
        Not allowed to choose neither """
        if state == 0 and not self.checkBox_6.isChecked():
            self.checkBox_6.setChecked(True)
            self.printLog("已选中「养成道具」")

    @pyqtSlot(int)
    def handleTabChanged(self, index: int):
        if index == 1 and not self._isMaterialScannerInitialized:
            self.initializeMaterialSignal.emit()
        self.logger.info(f"switched to [{self.tabWidget.tabText(index)}]")

    @pyqtSlot(int)
    def endInit(self, type_: int):
        if type_ == 1:
            self._isArtScannerInitialized = True
        elif type_ == 2:
            self._isMaterialScannerInitialized = True
        # tab 1
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_5.setEnabled(True)
        # tab 2
        self.pushButton_7.setEnabled(True)
        self.pushButton_8.setEnabled(True)

    @pyqtSlot()
    def onWorking(self):
        self.label.setMovie(self.gif)
        self.label_6.setMovie(self.gif)
        self.gif.start()

    @pyqtSlot()
    def endWorking(self):
        self.label.setPixmap(self.picOk)
        self.label_6.setPixmap(self.picOk)

    @pyqtSlot()
    def showHelpDlg(self):
        self._helpDlg.accept()
        self.logger.info("Help dialog shown.")
        point = self.rect().topRight()
        globalPoint = self.mapToGlobal(point)
        self._helpDlg.move(globalPoint)
        self._helpDlg.show()

    @pyqtSlot()
    def showAboutDlg(self):
        self.logger.info("About dialog shown.")
        dlg = AboutDlg(self)
        dlg.exec()

    @pyqtSlot()
    def showToolbox(self):
        if self._toolbox.isHidden():
            point = self.rect().topRight()
            globalPoint = self.mapToGlobal(point)
            self._toolbox.move(globalPoint)
            self._toolbox.show()

    @pyqtSlot()
    def selectedMona(self):
        self.logger.info("Mona selected.")
        self.checkBox.setChecked(True)
        self.checkBox_2.setChecked(True)
        self.checkBox_3.setChecked(False)
        self.checkBox_4.setChecked(False)
        self.checkBox_5.setChecked(False)

        self.spinBox.setValue(0)
        self.spinBox_2.setValue(20)

    @pyqtSlot()
    def selectedGenmo(self):
        self.logger.info("Genmo Calc selected.")
        self.checkBox.setChecked(True)
        self.checkBox_2.setChecked(False)
        self.checkBox_3.setChecked(False)
        self.checkBox_4.setChecked(False)
        self.checkBox_5.setChecked(False)

        self.spinBox.setValue(4)
        self.spinBox_2.setValue(20)

        QMessageBox.information(self,
                                "提示",
                                "<html>"
                                "您选择了「原魔计算器」格式，将在输出时自动过滤其不支持的数据。\n"
                                "(其仅支持导入"
                                "<span style=\"font-weight:600;color:#636399\">四词条</span>"
                                "的"
                                "<span style=\"font-weight:600;color:#636399e\">五星</span>"
                                "圣遗物)"
                                "</html>")

    @pyqtSlot()
    def selectedGOOD(self):
        self.logger.info("GOOD selected.")
        self.checkBox.setChecked(True)
        self.checkBox_2.setChecked(True)
        self.checkBox_3.setChecked(False)
        self.checkBox_4.setChecked(False)
        self.checkBox_5.setChecked(False)

        self.spinBox.setValue(0)
        self.spinBox_2.setValue(20)

    @pyqtSlot()
    def showExtraSettings(self):
        self.logger.info("Extra settings dialog shown.")
        dlg = ExtraSettingsDlg(self._settings, self)
        dlg.acceptSignal.connect(self.handleExtraSettings)
        dlg.exec()

    @pyqtSlot(str, bool)
    def showInputWindowName(self, window_name: str, isDup: bool):
        self.logger.info(f"Input window name dialog shown. window_name={window_name} isDup={isDup}")
        dlg = InputWindowDlg(self)
        if not isDup:
            dlg.label.setText(f"未找到标题为 {window_name} 的窗口，请输入窗口标题后重新捕获")
        else:
            dlg.label.setText(f"找到多个标题为 {window_name} 的窗口，请输入窗口标题后重新捕获")
        dlg.retVal.connect(self.handleInputWindowRet)
        dlg.exec()

    @pyqtSlot(str)
    def handleInputWindowRet(self, window_name):
        self.logger.info(f"Window name returned. window_name={window_name}")
        self.setWindowNameSignal.emit(window_name)

    @pyqtSlot(str)
    def printLog(self, log: str):
        self.logger.info(f"Info message shown. msg={log}")
        self.textBrowser_3.append(f'<font color="black">{log}</font>')
        QApplication.processEvents()

    @pyqtSlot(str)
    def printErr(self, err: str):
        self.logger.error(f"Error message shown. msg={err}")
        self.textBrowser_3.append(f'<font color="red">{err}</font>')
        QApplication.processEvents()

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
        self.logger.info(f"Start scan Artifacts. {info=}")

        self.setUIEnabled(False)

        self.startScanArtSignal.emit(info)

    @pyqtSlot()
    def startScanMaterial(self):
        info = {
            "options": [
                self.checkBox_6.isChecked(),
                self.checkBox_7.isChecked(),
            ],
            "delay": self.doubleSpinBox_2.value(),
            "exporter": (0 if self.radioButton_4.isChecked() else -1),
            "ExtraSettings": self._settings
        }
        self.logger.info(f"Start scan Materials. {info=}")
        self.setUIEnabled(False)

        self.startScanMaterialSignal.emit(info)

    def setUIEnabled(self, e: bool):
        self.pushButton.setEnabled(e)
        self.pushButton_8.setEnabled(e)

        self.checkBox.setEnabled(e)
        self.checkBox_2.setEnabled(e)
        self.checkBox_3.setEnabled(e)
        self.checkBox_4.setEnabled(e)
        self.checkBox_5.setEnabled(e)
        self.checkBox_6.setEnabled(e)
        self.checkBox_7.setEnabled(e)

        self.spinBox.setEnabled(e)
        self.spinBox_2.setEnabled(e)
        self.doubleSpinBox.setEnabled(e)
        self.doubleSpinBox_2.setEnabled(e)

        self.radioButton.setEnabled(e)
        self.radioButton_2.setEnabled(e)
        self.radioButton_3.setEnabled(e)
        self.radioButton_4.setEnabled(e)

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
        self.logger.info(f"Extra settings returned. ret={ret}")
        self._settings = ret
        self.groupBox_4.setEnabled(not self._settings['ExportAllFormats'])


class Worker(QObject):
    printLog = pyqtSignal(str)
    printErr = pyqtSignal(str)
    working = pyqtSignal()
    endWorking = pyqtSignal()
    endInit = pyqtSignal(int)
    endScan = pyqtSignal(str)
    showInputWindow = pyqtSignal(str, bool)

    def __init__(self):
        super(Worker, self).__init__()
        self.isQuit = False
        self.workingMutex = QMutex()
        self.cond = QWaitCondition()
        self.isInitialized = False
        self.isWindowCaptured = False

        self.logger = utils.logger

        self.windowName = '原神'
        # in initEngine
        self.game_info = None
        self.model = None
        self.bundle_dir = None

        # in initMaterialEngine
        self.model_m = None

        # init in scanArts
        self.art_id = 0
        self.saved = 0
        self.skipped = 0
        self.failed = 0
        self.star_dist = [0, 0, 0, 0, 0]
        self.star_dist_saved = [0, 0, 0, 0, 0]
        self.detectSettings = None

        # init in scanMaterials
        self.material_id = 0
        self.saved_material = 0
        self.failed_material = 0

    @pyqtSlot()
    def initArtEngine(self):
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
        self.log('初始化圣遗物 OCR 模型...')
        if len(sys.argv) > 1:
            self.bundle_dir = sys.argv[1]
        else:
            self.bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        self.model = ocr.OCR(model=os.path.join(self.bundle_dir,
                                                f'rcc/models_CHS/artifact_model_{config.TARGET_VERSION}.h5'))

        self.log('初始化完成')
        if self.isWindowCaptured:
            self.log('窗口已捕获，请检查行列数正确后开始扫描')
            self.log(f'行: {self.game_info.art_rows} , 列: {self.game_info.art_cols}')
            self.log('错误请重启游戏后重试')
        else:
            self.error('窗口未捕获，请在重新捕获窗口后开始扫描')

        self.log('开始扫描前请打开背包 - 圣遗物，并翻页至顶部')
        self.endWorking.emit()
        self.endInit.emit(1)

    @pyqtSlot()
    def initMaterialEngine(self):
        self.working.emit()

        # yield the thread
        time.sleep(0.5)
        self.log('初始化中，请稍候...')

        # 创建文件夹
        os.makedirs('materials', exist_ok=True)

        self.log('初始化材料 OCR 模型...')
        if len(sys.argv) > 1:
            self.bundle_dir = sys.argv[1]
        else:
            self.bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        self.model_m = ocr_m.OCR(model=os.path.join(self.bundle_dir,
                                                    f'rcc/models_CHS/material_model_{config.TARGET_VERSION}.h5'))

        self.log('初始化完成')
        if self.isWindowCaptured:
            self.log('窗口已捕获，请检查行列数正确后开始扫描')
            self.log(f'行: {self.game_info.art_rows} , 列: {self.game_info.art_cols}')
            self.log('错误请重启游戏后重试')
        else:
            self.error('窗口未捕获，请在重新捕获窗口后开始扫描')

        self.log('开始扫描前请打开背包，并翻页至顶部')
        self.endWorking.emit()
        self.endInit.emit(2)

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
    def scanMaterials(self, info: dict):
        self.working.emit()
        if not self.isWindowCaptured:
            self.error('窗口未捕获，请重新捕获窗口')
            self.endScan.emit('')
            self.endWorking.emit()
            return

        self.model_m.setScaleRatio(self.game_info.scale_ratio)
        self.detectSettings = info
        materialsDB = MaterialDatabase()
        materialScanner = MaterialScannerLogic(self.game_info)
        exporter = [materialsDB.exportGOODJSON]
        export_name = ['materials.GOOD.json']

        mouse.on_middle_click(materialScanner.interrupt)

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
        materialScanner.alignFirstRow()
        self.log('对齐完成，即将开始扫描')
        time.sleep(0.5)

        self.material_id = 0
        self.saved_material = 0
        self.failed_material = 0

        def autoCorrect(detected_info):
            detected_info['name'] = utils.material_name_auto_correct(detected_info['name'])

        def materialFilter(detected_info, detail_img, item_img):
            """
            0 - init value
            1 - skipped
            2 - saved
            3 - failed
            """
            status = 0

            try:
                autoCorrect(detected_info)
                self.log(f"识别到 [{detected_info['name']}]")
                detected_info['amount'] = utils.decodeValue(detected_info['amount'])
            except Exception as v:
                self.error("数值处理失败")
                self.logger.warning(f"[DecodeValue] error occurred")
                self.logger.exception(v)
                self.failed_material += 1
                status = 3

            if status != 0:
                pass
            elif materialsDB.add(detected_info, detail_img, item_img):
                self.log("已保存")
                self.logger.info(f"[MaterialDB] Scanned a Material."
                                 f" id: {self.material_id + 1} detected info: {detected_info}")
                self.saved_material += 1
                status = 2
            else:
                self.error("数值验证失败")
                self.logger.warning(f"[MaterialDB] Failed to scan a Material."
                                    f" id: {self.material_id + 1} detected info: {detected_info}")
                status = 3
                self.failed_material += 1
            self.material_id += 1
            saveImg(detected_info, detail_img, item_img, status)

        def saveImg(detected_info, detail_img, item_img, status):
            if self.detectSettings['ExtraSettings']['ExportAllImages']:
                if status == 3:
                    detail_img.save(f'materials/fail_{self.material_id}.png')
                    item_img.save(f'materials/item_fail_{self.material_id}.png')
                    s = json.dumps(detected_info, ensure_ascii=False)
                    with open(f"materials/fail_{self.material_id}.json", "wb") as f:
                        f.write(s.encode('utf-8'))
                else:
                    detail_img.save(f'materials/{self.material_id}.png')
                    item_img.save(f'materials/item_{self.material_id}.png')
                    s = json.dumps(detected_info, ensure_ascii=False)
                    with open(f"materials/{self.material_id}.json", "wb") as f:
                        f.write(s.encode('utf-8'))
            else:
                # export only failed
                if status == 3:
                    detail_img.save(f'materials/fail_{self.material_id}.png')
                    item_img.save(f'materials/item_fail_{self.material_id}.png')
                    s = json.dumps(detected_info, ensure_ascii=False)
                    with open(f"materials/fail_{self.material_id}.json", "wb") as f:
                        f.write(s.encode('utf-8'))

        def material_callback(detail_img, item_img):
            detectedInfo = self.model_m.detect_info(detail_img, item_img)
            materialFilter(detectedInfo, detail_img, item_img)
            if not self.material_id % self.game_info.art_cols:
                self.log(f"扫描: {self.material_id}")
                self.log(f"  - 保存: {self.saved_material}")
                self.log(f"  - 失败: {self.failed_material}")

        def scan_materials(target):
            start_row = 0
            self.log(f"开始扫描[{target}]")
            try:
                while True:
                    end_row = self.game_info.art_rows - 1
                    if start_row != 0:
                        end_row += 1
                    if materialScanner.scanner.stopped:
                        break
                    if not materialScanner.scanRows(rows=range(start_row, end_row),
                                                    callback=material_callback):
                        break
                    if start_row != 0:
                        break
                    start_row = (self.game_info.art_rows - 1 -
                                 materialScanner.scrollToRow(
                                     self.game_info.art_rows,
                                     max_scrolls=20,
                                     extra_scroll=int(self.game_info.art_rows > 5),
                                     interval=self.detectSettings['delay']))
                if materialScanner.scanner.stopped:
                    self.log(f'[{target}]扫描中断')
                else:
                    self.log(f'[{target}]扫描已完成')
            except Exception as e:
                self.logger.exception(e)
                self.error(repr(e))
                self.log('扫描出错，已停止')

        if info['options'][0]:
            materialScanner.clickCDIButton()
            scan_materials("养成道具")
        if info['options'][1]:
            materialScanner.clickMaterialButton()
            scan_materials("材料")

        if self.saved_material != 0:
            if info['ExtraSettings']['ExportAllFormats']:
                # export all formats
                list(map(lambda exp, name: exp(name), exporter, export_name))
            else:
                self.log(f"导出文件: {export_name[info['exporter']]}")
                exporter[info['exporter']](export_name[info['exporter']])
        self.log(f"扫描: {self.material_id}")
        self.log(f"  - 保存: {self.saved_material}")
        self.log(f"  - 失败: {self.failed_material}")
        self.log('失败结果将存储至 material 文件夹')

        del materialsDB
        self.endScan.emit(export_name[info['exporter']])
        self.endWorking.emit()

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

        def autoCorrect(detected_info):
            detected_info['name'] = utils.name_auto_correct(detected_info['name'])
            detected_info['type'] = utils.type_auto_correct(detected_info['type'])
            detected_info['equipped'] = utils.equipped_auto_correct(detected_info['equipped'])
            detected_info['setid'] = [i for i, v in enumerate(
                ArtsInfo.ArtNames) if detected_info['name'] in v][0]
            detected_info['main_attr_name'] = utils.attr_auto_correct(detected_info['main_attr_name'])
            for tag in sorted(detected_info.keys()):
                if "subattr_" in tag:
                    info_ = detected_info[tag].split('+')
                    detected_info[tag] = utils.attr_auto_correct(info_[0]) + "+" + info_[1]

        def artFilter(detected_info, art_img):
            """
            0 - init value
            1 - skipped
            2 - saved
            3 - failed
            """
            status = 0

            self.star_dist[detected_info['star'] - 1] += 1

            try:
                autoCorrect(detected_info)
                self.log(f"识别到 [{detected_info['name']}]")
                if detected_info['name'] in ArtsInfo.ArtNames[-1]:
                    self.log('[强化材料] 已跳过')
                    self.skipped += 1
                    status = 1
                else:
                    detectedLevel = utils.decodeValue(detected_info['level'])
                    detectedStar = utils.decodeValue(detected_info['star'])
            except Exception as v:
                self.error("数值处理失败")
                self.logger.warning(f"[DecodeValue] error occurred")
                self.logger.exception(v)
                self.failed += 1
                status = 3

            if status != 0:
                pass
            elif (self.detectSettings["ExtraSettings"]["FilterArtsByName"] and
                  (not self.detectSettings["ExtraSettings"]["Filter"][detected_info['setid']])):
                self.log("[名称过滤器] 已跳过")
                self.logger.info(f"[FilterArtsByName] Skipped a Artifact."
                                 f" id: {self.art_id + 1} detected info: {detected_info} set: {ArtsInfo.SetNames[detected_info['setid']]}")
                self.skipped += 1
                status = 1
            elif not ((self.detectSettings['levelMin'] <= detectedLevel <= self.detectSettings['levelMax']) and
                      (self.detectSettings['star'][detectedStar - 1])):
                self.log("[星级等级过滤器] 已跳过")
                self.logger.info(f"[FilterArtsByLevelAndStar] Skipped a Artifact."
                                 f" id: {self.art_id + 1} detected info: {detected_info}")
                self.skipped += 1
                status = 1
            elif artifactDB.add(detected_info, art_img):
                self.log("已保存")
                self.logger.info(f"[ArtifactDB] Saved a Artifact."
                                 f" id: {self.art_id + 1} detected info: {detected_info}")
                self.saved += 1
                status = 2
                self.star_dist_saved[detected_info['star'] - 1] += 1
            else:
                self.error("数值验证失败")
                self.logger.warning(f"[ArtifactDB] Failed to save a Artifact."
                                    f" id: {self.art_id + 1} detected info: {detected_info}")
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
            utils.logger.info(f"Detected info: {detectedInfo}")
            artFilter(detectedInfo, art_img)
            if not self.art_id % self.game_info.art_cols:
                self.log(f"扫描: {self.art_id}")
                self.log(f"  - 保存: {self.saved}")
                self.log(f"  - 失败: {self.failed}")
                self.log(f"  - 跳过: {self.skipped}")

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
            self.logger.exception(e)
            self.error(repr(e))
            self.log('扫描出错，已停止')

        if self.saved != 0:
            if info['ExtraSettings']['ExportAllFormats']:
                list(map(lambda exp, name: exp(name), exporter, export_name))
            else:
                self.log(f"导出文件: {export_name[info['exporter']]}")
                exporter[info['exporter']]({"path": export_name[info['exporter']],
                                            "exportLocation": info['ExtraSettings']['ExportLocationField']})
        self.log(f"扫描: {self.art_id}")
        self.log(f"  - 保存: {self.saved}")
        self.log(f"  - 失败: {self.failed}")
        self.log(f"  - 跳过: {self.skipped}")
        self.log('失败结果将存储至 artifacts 文件夹')

        self.log('星级: (保存 / 扫描)')
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
    try:
        app = QApplication(sys.argv)
        uiMain = UIMain()
        uiMain.show()
        app.exec()
    except Exception as excp:
        utils.logger.exception(excp)
        win32api.ShellExecute(0, 'open', 'cmd.exe',
                              r'/c echo Unhandled exception occurred. Please contact with the author. && pause',
                              None, 1)
