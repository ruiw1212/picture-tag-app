import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets


from Mylabel import MyLabel
from Tlabel import Tlabel


class cWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        # self.resize(2000,1000)
        self.names = []   # 用于存放所有标签的标注
        self.biaonum = 0   # 用户点击的矩形索引
        # 全局布局
        mlayout = QHBoxLayout()
        self.imagelabel = MyLabel()  # 创建图片标签
        self.imagelabel.setScaledContents(True)
        self.imagelabel.mouseReleaseSignal.connect(self.setText)  # 画矩形框完成时鼠标释放信号与槽连接
        self.imagelabel.mouseleftClickSignal1.connect(self.recname)  # 左键选中矩形框
        self.imagelabel.mouserightClickSignal.connect(self.clearone)  # 右键点击清除标注区颜色
        self.imagelabel.mouseleftClickSignal0.connect(self.rework)  # 左键

        # 局部布局
        selayout = QVBoxLayout()
        self.seWidget = QWidget()

        editlayout = QVBoxLayout()  # 内容列表
        self.eWidget = QWidget()  # 内容区控件
        self.eWidget.setStyleSheet('''QWidget{background-color:rgb(255, 255, 255);}''')  # 局部布局背景为白色
        self.textlabel = QLabel()  # 设置标注区标题标签
        # self.linedit = QLineEdit()
        self.textlabel.setText('<font color=blue face="黑体" size=5>标注区</font>')
        editlayout.addWidget(self.textlabel,0,Qt.AlignTop | Qt.AlignCenter)
        self.textlabels = []  # 设置标注标签列表
        for i in range(0,25):   # 建立标注控件
            self.textlabels.append(Tlabel())
            self.textlabels[i].j = i
            self.textlabels[i].mouseDoubleClickSignal.connect(self.rname)  # 每个标注标签信号连接rname槽函数
        # self.CTextlabels()
        for la in self.textlabels:
            editlayout.addWidget(la,0,Qt.AlignTop)  # 水平居中对齐
        # editlayout.addWidget(self.linedit, 0, Qt.AlignTop)
        self.eWidget.setLayout(editlayout)

        worklayout = QVBoxLayout()   # 工作区
        self.wWidget = QWidget()   # 工作区控件
        self.wWidget.setStyleSheet('''QWidget{background-color:rgb(255, 255, 255);}''')  # 局部布局背景为白色
        self.textlabel1 = QLabel()
        self.textlabel1.setText('<font color=blue face="黑体" size=5>工作区</font>')
        self.workedit = QLineEdit()
        font = self.workedit.font()  # lineedit current font
        font.setPointSize(15)  # change it's size
        self.workedit.setFont(font)  # set font
        self.worklabel = QLabel()
        self.definebtn = QPushButton("确认修改")
        self.delebtn = QPushButton("删除标注")
        self.definebtn.setStyleSheet('''QWidget{background-color:rgb(240, 240, 240);}''')
        self.delebtn.setStyleSheet('''QWidget{background-color:rgb(240, 240, 240);}''')
        self.definebtn.clicked.connect(self.workname)
        self.delebtn.clicked.connect(self.delerect)
        worklayout.addWidget(self.textlabel1, 1, Qt.AlignTop | Qt.AlignCenter)
        worklayout.addWidget(self.worklabel,5,Qt.AlignVCenter)
        worklayout.addWidget(self.workedit, 5,Qt.AlignVCenter)  # 垂直居中
        worklayout.addWidget(self.definebtn, 1, Qt.AlignVCenter)  # 垂直居中
        worklayout.addWidget(self.delebtn, 1, Qt.AlignVCenter)  # 垂直居中
        self.workedit.setDisabled(True)
        self.delebtn.setDisabled(True)
        self.definebtn.setDisabled(True)
        self.wWidget.setLayout(worklayout)

        # 右侧局部布局工作区与标注区
        selayout.addWidget(self.wWidget,1)
        selayout.addWidget(self.eWidget,3)
        self.seWidget.setLayout(selayout)

        # 全局布局添加
        mlayout.addWidget(self.imagelabel,5,Qt.AlignCenter | Qt.AlignVCenter)  # 将图片label居中放到水平布局上 Qt.AlignCenter | Qt.AlignVCenter
        # self.imagelabel.adjustSize()
        self.imagelabel.setScaledContents(True)
        mlayout.addWidget(self.seWidget,1)  # 添加局部布局控件
        # mlayout.addWidget(self.textedit, 2)  # 将文本框放在水平布局上
        self.setLayout(mlayout)

    # 绘制矩形框后编写标注 槽函数
    def setText(self,text,i):
        self.definebtn.setDisabled(False)
        self.delebtn.setDisabled(False)
        for j in range(0,i-1):
            self.textlabels[j].setStyleSheet('''QWidget{background-color:rgb(240, 240, 240);}''')
        self.textlabels[i].setText(text)
        # self.textlabel[i].setFont(font)
        self.textlabels[i].setFont(QFont("e", 10))   # 设置字体的大小
        # self.textlabels[i].setStyleSheet('''QWidget{background-color:rgb(240, 240, 240);}''')
        self.textlabels[i].repaint()
        self.names.append(text)

    # 双击标注标签修改标注内内容 槽函数
    def rname(self,text,i):
        self.names[i] = text
        # print(self.names[i] + str(i))

    # 单击标注框显示对应标注内容 槽函数
    def recname(self,i,j):
        for x in range(0,j+2):
            self.textlabels[x].setStyleSheet('''QWidget{background-color:rgb(240, 240, 240);}''')
        if i > 0:
            self.textlabels[j].setStyleSheet('''QWidget{background-color:rgb(240, 240, 240);}''')
        self.textlabels[i].setStyleSheet('''QWidget{background-color:rgb(255, 236, 139);}''')

    # 清除选中文字框
    def clearone(self,i):
        for j in range(0,i):
            self.textlabels[j].setStyleSheet('''QWidget{background-color:rgb(240, 240, 240);}''')
        """
        text, ok = QInputDialog.getText(self, '标注', '', QtWidgets.QLineEdit.Normal, t)
        if ok and text:
            self.textlabels[i].setText(text)
            self.textlabels[i].setStyleSheet('''QWidget{background-color:rgb(240, 240, 240);}''')
            self.rname(text,i)
        else:
            self.textlabels[i].setStyleSheet('''QWidget{background-color:rgb(240, 240, 240);}''')
        """

    # 工作区操作
    def rework(self,i):
        self.biaonum = i
        self.definebtn.setDisabled(False)
        self.delebtn.setDisabled(False)
        self.workedit.setDisabled(False)
        self.worklabel.setStyleSheet('''QWidget{background-color:rgb(240, 240, 240);}''')
        self.worklabel.setText(self.names[i])
        self.workedit.setText(self.names[i])
        self.worklabel.setFont(QFont("e", 10))

    # 工作区确认修改
    def workname(self):
        text = self.workedit.text()
        self.worklabel.setText(text)
        self.textlabels[self.biaonum].setText(text)
        self.textlabels[self.biaonum].setText(text)
        self.names[self.biaonum] = text   # 更改标注列表
        self.worklabel.repaint()

    # 删除矩形框
    def delerect(self):
        self.worklabel.setText('')
        self.workedit.setText('')
        self.worklabel.repaint()
        print(self.imagelabel.i)
        for j in range(self.biaonum, self.imagelabel.i):
            self.textlabels[j].setText(self.textlabels[j+1].text())
        self.textlabels[self.imagelabel.i].setText('')
        self.textlabels[self.imagelabel.i].setStyleSheet('''QWidget{background-color:rgb(255, 255, 255);}''')
        # 修改保存内容
        del self.imagelabel.rects[self.biaonum]
        del self.names[self.biaonum]
        self.imagelabel.x0,x1,y0,y1 = 0,0,0,0
        self.imagelabel.i = self.imagelabel.i - 1
        self.imagelabel.repaint()






if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = cWidget()
    # main.center()
    main.show()
    sys.exit(app.exec_())


"""
if event.buttons() == QtCore.Qt.LeftButton:
            self.left_flag = True
        if event.buttons() == QtCore.Qt.RightButton:
            self.right_flag = True
"""

