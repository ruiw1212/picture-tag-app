
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets


class Tlabel(QLabel):
    mouseDoubleClickSignal = QtCore.pyqtSignal(str, int)  # 设置标注完成的信号

    def __init__(self):
        super(QLabel, self).__init__()
        self.j = -1  # 设置索引

    def mouseDoubleClickEvent(self, event):
        # self.setStyleSheet('''QWidget{background-color:rgb(123, 123, 99);}''')
        t = self.text()  # 默认已输入文本
        text, ok = QInputDialog.getText(self, '标注','',QtWidgets.QLineEdit.Normal,t)
        if ok and text:
            self.setText(text)
            self.mouseDoubleClickSignal.emit(text,self.j)
            # self.setStyleSheet('''QWidget{background-color:rgb(240, 240, 240);}''')
