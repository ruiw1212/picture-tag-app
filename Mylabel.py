from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore


class MyLabel(QLabel):
    mouseReleaseSignal = QtCore.pyqtSignal(str, int)  # 设置标注完成的信号
    mouseleftClickSignal1 = QtCore.pyqtSignal(int, int)  # 选中矩形框传递给标注区信号
    mouserightClickSignal = QtCore.pyqtSignal(int)  # 右键点击矩形框信号
    mouseleftClickSignal0 = QtCore.pyqtSignal(int)  # 左键点击传递给工作区信号

    def __init__(self):
        super(QLabel, self).__init__()
        # 截图时鼠标按下下松开坐标
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        # 其他功能鼠标按下松开坐标
        self.xx0 = 0
        self.yy0 = 0
        self.xx1 = 0
        self.yy1 = 0

        # 两次鼠标坐标之差
        self.diffex = 0
        self.diffey = 0
        # self.flag = False   # 运行截图功能是否开始截图

        self.rects = []  # 用于存储所有矩形的长宽数据
        self.cutflag = False  # 是否进行截图功能
        self.cancelflag = False  # 用户是否在标注时取消
        self.left_flag = False  # 鼠标左键是否点击
        self.right_flag = False  # 鼠标右键是否点击
        self.moveflag = False  # 用户是否移动矩形
        self.bigflag = False  # 用户是否放大矩形
        self.colorflag = False  # 判断用户是否选中某个矩形
        self.firstflag = True  # 用户是否第一次点击矩形
        self.ifmove = False  # 用户是否移动鼠标，防止矩阵被删除

        self.i = 0  # 现有矩形框数量-1
        self.lastwhich = 0  # 选中的上一个矩形框
        self.which = 0  # 选中哪个矩形框
        self.whichdot = 0  # 鼠标左键点击哪个点

    # 鼠标点击事件
    def mousePressEvent(self, event):
        # 鼠标点击则把点击设为True
        if event.buttons() == QtCore.Qt.LeftButton:
            self.left_flag = True
        if event.buttons() == QtCore.Qt.RightButton:
            self.right_flag = True

        # self.colorflag = True

        # 主菜单点击截图功能后左键点击进行截图
        if self.cutflag:
            self.x0 = 0
            self.x1 = 0
            self.y0 = 0
            self.y1 = 0
            if self.left_flag:
                # print(event.x())
                self.x0 = event.x()
                self.y0 = event.y()

        # 直接左键矩形框移动或放大
        if self.left_flag:
            self.xx0 = event.x()
            self.yy0 = event.y()
            # 遍历矩形列表，判断左键单击位置是否在某个矩形框或四角的点内
            for recs in self.rects:

                # 矩形框，移动
                if recs[0] - 6 <= self.xx0 <= recs[0] + 6 and \
                        recs[1] + 0.5 * recs[3] - 6 <= self.yy0 <= 0.5 * recs[3] + recs[1] + 6:  # 左
                    self.which = self.rects.index(recs)  # which为矩形框索引
                    # print('i')
                    self.moveflag = True
                    # print('move1')
                if recs[2] + recs[0] - 6 <= self.xx0 <= recs[2] + recs[0] + 6 and \
                        recs[1] + 0.5 * recs[3] - 6 <= self.yy0 <= 0.5 * recs[3] + recs[1] + 6:  # 右
                    self.which = self.rects.index(recs)  # which为矩形框索引
                    # print('i')
                    self.moveflag = True
                    # print('move2')

                #  选中矩形框
                if recs[0] - 6 <= self.xx0 <= recs[2] + recs[0] + 6 and recs[1] - 6 <= self.yy0 <= recs[3] + recs[
                    1] + 6:
                    self.which = self.rects.index(recs)
                    self.colorflag = True
                    # print(self.colorflag)
                    # print('double')

                    # 如果是第一次点击
                    if self.firstflag:
                        self.lastwhich = self.which  # 保存前一个点击的索引
                        self.firstflag = False
                    self.mouseleftClickSignal1.emit(self.which, self.i - 1)  # 给标注区label发送信号
                    # print(self.lastwhich)
                    self.lastwhich = self.which  # 保存前一个点击的索引

                # 右下点，放大
                if recs[0] + recs[2] - 6 <= self.xx0 <= recs[2] + recs[0] + 6 and \
                        recs[1] + recs[3] - 6 <= self.yy0 <= recs[3] + recs[1] + 6:
                    self.which = self.rects.index(recs)  # which为矩形框索引
                    self.whichdot = 3
                    self.bigflag = True
                    # print('yes3')
                # 左上点
                elif recs[0] - 6 <= self.xx0 <= recs[0] + 6 and \
                        recs[1] - 6 <= self.yy0 <= recs[1] + 6:
                    self.which = self.rects.index(recs)  # which为矩形框索引
                    self.whichdot = 0
                    self.bigflag = True
                    # print('yes0')
                # 左下点
                elif recs[0] - 6 <= self.xx0 <= recs[0] + 6 and \
                        recs[1] + recs[3] - 6 <= self.yy0 <= recs[3] + recs[1] + 6:
                    self.which = self.rects.index(recs)  # which为矩形框索引
                    self.whichdot = 2
                    self.bigflag = True
                    # print('yes2')
                # 右上点
                elif recs[0] + recs[2] - 6 <= self.xx0 <= recs[2] + recs[0] + 6 and \
                        recs[1] - 6 <= self.yy0 <= recs[1] + 6:
                    self.which = self.rects.index(recs)  # which为矩形框索引
                    self.whichdot = 1
                    self.bigflag = True
                    #  print('yes1')

        # 右键选中矩形框进行修改
        if self.right_flag:
            self.mouserightClickSignal.emit(self.i + 1)

    # 鼠标释放事件
    def mouseReleaseEvent(self, event):

        # 截图状态下左键释放进行标注
        if self.cutflag:
            if self.left_flag:
                # if event.buttons() == QtCore.Qt.LeftButton:
                rec = [self.x0, self.y0, self.x1 - self.x0, self.y1 - self.y0]
                print(rec)
                text, ok = QInputDialog.getText(self, '标注', '')
                if ok and text:
                    self.rects.append(rec)  # 每次释放鼠标，将这次绘制矩形存入列表中
                    self.i = len(self.rects) - 1
                    self.mouseReleaseSignal.emit(text, self.i)  # 如果选择确认就把标注的内容作为信号发送
                    self.mouseleftClickSignal1.emit(self.i, self.i - 1)  # 将目前的标注框选中

                else:
                    self.cancelflag = True  # 用户取消，将标志设为True

                self.cutflag = False  # 每次使用截图功能只能画一个图

        # 移动状态下左键释放进行移动
        if self.moveflag or self.bigflag:
            if self.left_flag and self.ifmove:
                self.moveflag = False
                self.bigflag = False
                # 更新矩形数据
                del self.rects[self.which]

                # print([self.x0, self.y0, self.x1 - self.x0, self.y1 - self.y0])
                self.rects.insert(self.which, [self.x0, self.y0, self.x1 - self.x0, self.y1 - self.y0])
                self.ifmove = False
                self.repaint()

        # 仅选中单击某个矩形框
        if self.colorflag and self.left_flag:
            # 将点击的矩形框填充颜色
            if not self.ifmove:
                self.x0 = self.rects[self.which][0]
                self.y0 = self.rects[self.which][1]
                self.x1 = self.rects[self.which][2] + self.x0
                self.y1 = self.rects[self.which][3] + self.y0
                self.repaint()
                self.colorflag = False

                # print([self.x0,self.y0,self.x1,self.y1])
                if self.firstflag:
                    self.lastwhich = self.which  # 保存前一个点击的索引
                    self.firstflag = False
                self.mouseleftClickSignal1.emit(self.which, self.i - 1)  # 给标注区label发送信号
                # print(self.lastwhich)
                self.lastwhich = self.which  # 保存前一个点击的索引
                self.mouseleftClickSignal0.emit(self.which)  # 发送工作区信号

        self.left_flag = False
        self.right_flag = False

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        # 截图状态下单击左键拉动绘制矩形框
        if self.cutflag:
            if self.left_flag:
                self.x1 = event.x()
                self.y1 = event.y()
                self.update()

        # 移动放大状态下单击左键将矩形框位置移动放大
        if self.left_flag:
            # 找到前后矩形坐标值差
            self.xx1 = event.x()
            self.yy1 = event.y()
            self.diffex = self.xx1 - self.xx0
            self.diffey = self.yy1 - self.yy0
            self.update()

            if self.moveflag:
                self.ifmove = True
                # 更新响应矩形数据
                self.x0 = self.rects[self.which][0] + self.diffex
                self.y0 = self.rects[self.which][1] + self.diffey
                self.x1 = self.rects[self.which][2] + self.rects[self.which][0] + self.diffex
                self.y1 = self.rects[self.which][3] + self.rects[self.which][1] + self.diffey
                # del self.rects[self.which]
                # print('m')
                self.update()
                # self.repaint()

            if self.bigflag:
                self.ifmove = True
                if self.whichdot == 3:  # 左上角点x0，y0不变
                    self.x0 = self.rects[self.which][0]
                    self.y0 = self.rects[self.which][1]
                    self.y1 = self.rects[self.which][3] + self.rects[self.which][1] + self.diffey
                    self.x1 = self.rects[self.which][2] + self.rects[self.which][0] + self.diffex
                    self.update()

                elif self.whichdot == 0:  # x1，y1不变
                    self.x0 = self.rects[self.which][0] + self.diffex
                    self.y0 = self.rects[self.which][1] + self.diffey
                    self.x1 = self.rects[self.which][2] + self.rects[self.which][0]
                    self.y1 = self.rects[self.which][3] + self.rects[self.which][1]
                    self.update()

                elif self.whichdot == 2:  # x1，y0不变
                    self.x0 = self.rects[self.which][0] + self.diffex
                    self.y0 = self.rects[self.which][1]
                    self.x1 = self.rects[self.which][2] + self.rects[self.which][0]
                    self.y1 = self.rects[self.which][3] + self.rects[self.which][1] + self.diffey
                    self.update()

                elif self.whichdot == 1:  # x0，y1不变
                    self.x0 = self.rects[self.which][0]
                    self.x1 = self.rects[self.which][2] + self.rects[self.which][0] + self.diffex
                    self.y0 = self.rects[self.which][1] + self.diffey
                    self.y1 = self.rects[self.which][3] + self.rects[self.which][1]
                    self.update()

        # self.ifmove = True

    def mouseDoubleClickEvent(self, event):
        pass

    # 绘制事件
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.begin(self)
        if self.rects != []:
            for recs in self.rects:  # 先遍历矩形列表中已有矩形，画出所有已画矩形
                self.drawrrect(painter, recs[0], recs[1], recs[2], recs[3])
                self.drawdot(painter, recs[0], recs[1], recs[2] + recs[0], recs[3] + recs[1])

        # 画现在再画的矩形
        self.drawdot(painter, self.x0, self.y0, self.x1, self.y1)
        self.drawrrect(painter, self.x0, self.y0, (self.x1 - self.x0), (self.y1 - self.y0))
        painter.setBrush(QBrush(Qt.Dense5Pattern))
        rect = QRect(self.x0, self.y0, (self.x1 - self.x0), (self.y1 - self.y0))
        painter.drawRect(rect)

        if self.cancelflag:
            self.cancelflag = False
            # print('re')
            self.x0, self.y0, self.x1, self.y1 = 0, 0, 0, 0
            self.repaint()

        painter.end()

    # 画矩形四角的点
    def drawdot(self, painter, x0, y0, x1, y1):
        painter.setPen(QPen(Qt.red, 1, Qt.SolidLine))
        brush_ellipse = QBrush(Qt.red)
        painter.setBrush(brush_ellipse)
        painter.drawEllipse(x0 - 6, y0 - 6, 12, 12)  # (startx, starty, w, h) 左上
        painter.drawEllipse(x1 - 6, y0 - 6, 12, 12)  # (startx, starty, w, h) 右上
        painter.drawEllipse(x0 - 6, y1 - 6, 12, 12)  # (startx, starty, w, h) 左上
        painter.drawEllipse(x1 - 6, y1 - 6, 12, 12)  # (startx, starty, w, h) 右下
        painter.drawEllipse(x0 - 6, (y0 + y1) / 2 - 6, 12, 12)
        painter.drawEllipse(x1 - 6, (y0 + y1) / 2 - 6, 12, 12)
        painter.setBrush(Qt.NoBrush)  # 重新设置颜色为不填充

    # 绘制矩形框
    def drawrrect(self, painter, x0, y0, w, h):
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        rect = QRect(x0, y0, w, h)
        painter.drawRect(rect)
        # painter.setBrush(Qt.NoBrush)
        # self.colorflag = False

    def judge(self, x, y):
        pass
