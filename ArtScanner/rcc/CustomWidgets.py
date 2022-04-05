import os

from PyQt5.QtGui import QDropEvent
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import pyqtSignal


class DropTextEdit(QTextEdit):
    dropEventSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(DropTextEdit, self).__init__(parent)
        self.setAcceptDrops(True)

    def dropEvent(self, e: QDropEvent) -> None:
        if e.mimeData().hasUrls():
            urls = e.mimeData().urls()
            if len(urls) != 1:
                return
            file_path = urls[0].toLocalFile()

            if os.path.isfile(file_path):
                self.dropEventSignal.emit(file_path)

