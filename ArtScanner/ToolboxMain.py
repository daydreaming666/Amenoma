import os.path
import sys
import json

from PyQt5.QtCore import pyqtSlot

from art_saver import ArtDatabase

from ArtsInfo import (ArtNames, TypeNames, MainAttrNames, SubAttrNames,
                      AttrNamesGenshinArt, SetNamesGenshinArt, TypeNamesGenshinArt,
                      AttrNamesMingyuLab, SetNamesMingyuLab, TypeNamesMingyuLab,
                      AttrNamesGOOD, SetNamesGOOD, TypeNamesGOOD,
                      MainAttrValue, UsersCHS)

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from rcc import ToolboxMainWindow

from utils import logger

monaAttrMap = {v: k for k, v in AttrNamesGenshinArt.items()}
genmoAttrMap = {v: k for k, v in AttrNamesMingyuLab.items()}
goodAttrMap = {v: k for k, v in AttrNamesGOOD.items()}

userMap = {v: k for k, v in UsersCHS.items()}

genmoPercentageValues = ["critRate", "critDamage", "percentATK", "energyRecharge", "percentHP", "percentDEF",
                         "physicalDamage", "geoDamage", "anemoDamage", "cryoDamage", "hydroDamage", "pyroDamage",
                         "electroDamage"]


class ToolboxUiMain(QMainWindow, ToolboxMainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(ToolboxUiMain, self).__init__(parent)
        self.setupUi(self)

        self.isConverted = False
        self.outputFormat = ""
        self.inputFormat = ""
        self.inputPath = "./"
        self.outputPath = "./"

        self.textEdit.dropEventSignal.connect(self.handleOpenFile)

        self.pushButton_2.clicked.connect(self.openFileButtonClicked)

        self.pushButton.clicked.connect(self.convert)
        self.pushButton_3.clicked.connect(self.handleCopyButton)
        self.pushButton_4.clicked.connect(self.handleOutputButton)

    @pyqtSlot()
    def handleOutputButton(self):
        filename = ""
        if self.outputFormat == "mona":
            filename = "artifacts.genshinart.json"
        elif self.outputFormat == "genmo":
            filename = "artifacts.genmocalc.json"
        elif self.outputFormat == "good":
            filename = "artifacts.GOOD.json"
        filepath = QFileDialog.getSaveFileName(self, "导出文件", self.outputPath + "/" + filename,
                                               "JSON (*.json);;Text (*.txt)")
        if filepath[0]:
            self.outputPath = os.path.dirname(filepath[0])
            with open(filepath[0], "w", encoding="utf-8") as f:
                data = self.textEdit_2.toPlainText()
                f.write(data)

    @pyqtSlot()
    def handleCopyButton(self):
        text = self.textEdit_2.toPlainText()
        QApplication.clipboard().setText(text)

    @staticmethod
    def monaIter(data):
        flower = data['flower']
        feather = data['feather']
        sand = data['sand']
        cup = data['cup']
        head = data['head']
        all_data = flower + feather + sand + cup + head
        for item in all_data:
            res = {
                'name': ArtNames[SetNamesGenshinArt.index(item['setName'])][
                    TypeNamesGenshinArt.index(item['position'])],
                'type': TypeNames[TypeNamesGenshinArt.index(item['position'])],
                'locked': False,
                'equipped': "",
                'setid': SetNamesGenshinArt.index(item['setName']),
                'level': item['level'],
                'star': item['star'],
                'main_attr_name': MainAttrNames[monaAttrMap[item['mainTag']['name']]],
                'main_attr_value': item['mainTag']['value']}
            for i, v in enumerate(item['normalTags']):
                res['subattr_{}'.format(i + 1)] = SubAttrNames[monaAttrMap[v['name']]] + '+' \
                                                  + (str(v['value'])
                                                     if v['value'] > 1
                                                     else ("{:.1f}%".format(v['value'] * 100)))
            yield res

    @staticmethod
    def genmoIter(data):
        for item in data:
            res = {'name': ArtNames[SetNamesMingyuLab.index(item['asKey'])][TypeNamesMingyuLab.index(item['slot'])],
                   'type': TypeNames[TypeNamesMingyuLab.index(item['slot'])], 'locked': False, 'equipped': "",
                   'setid': SetNamesMingyuLab.index(item['asKey']), 'level': item['level'], 'star': item['rarity'],
                   'main_attr_name': MainAttrNames[genmoAttrMap[item['mainStat']]],
                   'main_attr_value': MainAttrValue[item['rarity']][genmoAttrMap[item['mainStat']]][item['level']]
                   }
            for i in range(1, 5):
                res[f'subattr_{i}'] = SubAttrNames[genmoAttrMap[item[f'subStat{i}Type']]] + '+' \
                                      + item[f'subStat{i}Value'] \
                                      + ("%" if item[f'subStat{i}Type'] in genmoPercentageValues else "")
            yield res

    @staticmethod
    def goodIter(data):
        for item in data['artifacts']:
            res = {'name': ArtNames[SetNamesGOOD.index(item['setKey'])][TypeNamesGOOD.index(item['slotKey'])],
                   'type': TypeNames[TypeNamesGOOD.index(item['slotKey'])], 'locked': item['lock'],
                   'equipped': (userMap[item['location']]
                                if (item['location'] != "" and item['location'] != "None")
                                else ""), 'setid': SetNamesGOOD.index(item['setKey']), 'level': item['level'],
                   'star': item['rarity'], 'main_attr_name': MainAttrNames[goodAttrMap[item['mainStatKey']]],
                   'main_attr_value': MainAttrValue[item['rarity']][goodAttrMap[item['mainStatKey']]][item['level']]}
            for i in range(1, len(item['substats']) + 1):
                res[f'subattr_{i}'] = SubAttrNames[goodAttrMap[item['substats'][i - 1]['key']]] + '+' \
                                      + (("{:.1f}%".format(item['substats'][i - 1]['value']))
                                         if item['substats'][i - 1]['key'].endswith('_')
                                         else ("{:d}".format(item['substats'][i - 1]['value'])))
            yield res

    @pyqtSlot()
    def openFileButtonClicked(self):
        filename = ""
        if self.inputFormat == 'mona':
            filename = "artifacts.genshinart.json"
        elif self.inputFormat == 'genmo':
            filename = "artifacts.genmocalc.json"
        elif self.inputFormat == 'good':
            filename = "artifacts.GOOD.json"
        filepath = QFileDialog.getOpenFileName(self, '打开文件', self.inputPath + "/" + filename,
                                               'JSON Files (*.json);;All Files (*)')
        if filepath[0]:
            self.inputPath = filepath[0].split('/')[:-1]
            self.handleOpenFile(filepath[0])

    @pyqtSlot(str)
    def handleOpenFile(self, path: str):
        logger.info("Open file: {}".format(path))
        with open(path, 'r', encoding='utf-8') as f:
            self.inputPath = os.path.dirname(path)
            try:
                data = json.load(f)
                formatted_json = json.dumps(data, indent=2, ensure_ascii=False)
                self.textEdit.setText(formatted_json)
            except json.JSONDecodeError as e:
                self.textEdit.setText("<html><font color='red'>"
                                      "json 解码错误，请检查文件: \n"
                                      f"{e}"
                                      "</font></html>")

    @pyqtSlot()
    def convert(self):
        source_format = self.comboBox.currentText()
        target_format = self.comboBox_2.currentText()

        source_data = self.textEdit.toPlainText()

        try:
            data = json.loads(source_data)
        except json.JSONDecodeError as e:
            self.textEdit_2.setText("<html><font color='red'>"
                                    "json 解码错误，请检查文件: \n"
                                    f"{e}"
                                    "</font></html>")
            return

        generator = None
        if source_format == '莫娜占卜铺':
            self.inputFormat = 'mona'
            generator = self.monaIter(data)
        elif source_format == '原魔计算器':
            self.inputFormat = 'genmo'
            generator = self.genmoIter(data)
        elif source_format == 'GOOD':
            self.inputFormat = 'good'
            generator = self.goodIter(data)
        try:
            db = ArtDatabase()
            for item in generator:
                db.add(item, None, raise_error=True)
        except Exception as e:
            self.textEdit_2.setText("<html><font color='red'>"
                                    "数据错误，检查数据: \n"
                                    f"{e}"
                                    "</font></html>")
            self.isConverted = False
            logger.exception(e)
            return

        self.isConverted = True
        output_data = {}
        if target_format == '莫娜占卜铺':
            output_data = db.exportGenshinArtJSON("")
            self.outputFormat = 'mona'
        elif target_format == '原魔计算器':
            output_data = db.exportGenmoCalcJSON("")
            self.outputFormat = 'genmo'
        elif target_format == 'GOOD':
            output_data = db.exportGOODJSON("")
            self.outputFormat = 'good'

        self.textEdit_2.setText(json.dumps(output_data, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    uiMain = ToolboxUiMain()
    uiMain.show()
    app.exec()
