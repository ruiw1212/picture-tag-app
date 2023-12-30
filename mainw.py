import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets

import xml.etree.ElementTree as ET

from PIL import Image
import cv2

from cenWidget import cWidget  # 引入主控件


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        screen = QDesktopWidget().screenGeometry()  # 得到屏幕坐标

        # self.statusBar = QStatusBar()
        # self.resize(screen.width(), screen.height())  # 全屏
        self.resize(2000,1200)
        self.setWindowTitle('labelimg')
        self.initmenu()  # 创建菜单栏
        self.inittoobar()  # 创建工具栏
        self.Cutflag = False  # 是否使用截图功能

        mainframe = cWidget()  # 创建主窗口中心控件
        self.setCentralWidget(mainframe)
        self.move(0, 0)

        self.xmlrect = []  # 临时存储矩形数据，解析xml树

        # 打开xml文件时原始数据，用于判断是否有修改
        self.origtext = []
        self.origrect = []

        self.filekind = 0  # 判断打开文件为图片还是xml，0位图片，1位xml
        self.scaleFactor = 1.0

    def initmenu(self):
        bar = self.menuBar()  # 添加菜单栏

        file = bar.addMenu("文件")  # 菜单栏第一项为文件
        Open = file.addAction('打开')  # 文件的子菜单打开，保存，另存为
        Open.setShortcut("Ctrl+O")
        self.Save = file.addAction('保存')
        self.Save.setShortcut("Ctrl+S")
        self.Save.setDisabled(True)
        self.Saveas = file.addAction("另存为")
        self.Saveas.setShortcut("Ctrl+Shift+S")
        self.Saveas.setDisabled(True)

        self.Save.triggered.connect(self.buildxml)
        Open.triggered.connect(self.loadfile)  # open连接到loadfile
        self.Saveas.triggered.connect(self.buildxml)

        edit = bar.addMenu("编辑")  # 菜单栏第二项为编辑
        self.Create = edit.addAction("创建矩形框")  # 编辑第一项创建矩形框
        self.Create.setShortcut("Ctrl+R")
        self.Create.triggered.connect(self.imagecut)

        view = bar.addMenu("视图")  # 菜单栏第三项为视图
        self.zoomi = view.addAction("放大图形")
        self.zoomi.setShortcut("Ctrl+B")
        self.zoomou = view.addAction("缩小图形")
        self.zoomou.setShortcut("Ctrl+L")
        self.fittowindow = view.addAction("适应窗口")
        self.fitnorma = view.addAction("正常大小")
        self.zoomi.triggered.connect(self.zoominn)
        self.zoomou.triggered.connect(self.zoomoutt)
        self.fittowindow.triggered.connect(self.fitwin)
        self.fitnorma.triggered.connect(self.fitnorm)

        Help = bar.addMenu("帮助")
        inf = Help.addAction("说明")
        inf.triggered.connect(self.openhelp)

    def inittoobar(self):
        tb1 = self.addToolBar("File")  # 创建工具栏

        self.save1 = QAction(QIcon("./resource/Save.ico"), '保存', self)  # 工具栏第一个工具保存
        self.save1.triggered.connect(self.buildxml)
        self.save1.setDisabled(True)
        tb1.addAction(self.save1)  # 添加保存到工具栏

        open1 = QAction(QIcon("./resource/Open File.ico"), '打开', self)  # 工具栏第二个工具打开
        open1.triggered.connect(self.loadfile)  # open连接到loadimage
        tb1.addAction(open1)

        self.edit = QAction(QIcon('./resource/Desktop.ico'), '截图编辑', self)  # 工具栏第三个工具编辑
        tb1.addAction(self.edit)
        self.edit.triggered.connect(self.imagecut)

        self.zoomin = QAction(QIcon("./resource/Zoom In.ico"), '放大图片', self)  # 工具栏第四个工具放大
        self.zoomin.triggered.connect(self.zoominn)
        tb1.addAction(self.zoomin)

        self.zoomout = QAction(QIcon("./resource/Zoom Out.ico"), '缩小图片', self)  # 工具栏第五个工具缩小
        self.zoomout.triggered.connect(self.zoomoutt)
        tb1.addAction(self.zoomout)

        tb1.setStyleSheet("QToolBar{spacing:15px;}")  # 设置工具栏间隔

    # 退出程序
    def closeEvent(self, event):
        # 判断用户是否修改内容
        if (self.origtext == self.centralWidget().names) and (self.origrect == self.centralWidget().imagelabel.rects):
            event.accept()
        else:
            reply = QtWidgets.QMessageBox.warning(self, '警告', '你有未保存的内容,是否仍要退出',
                                                  QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

    # 打开文件图片或者xml
    def loadfile(self):
        fname, _ = QFileDialog.getOpenFileName(self, '打开文件', '.', '图像文件(*.png *.bmp *.jpeg *.jpg *.xml)')  # 第三个参数为默认路径(选择当前）
        if fname == '':
            return
        self.Save.setEnabled(True)   # 设置保存功能可用
        self.save1.setEnabled(True)
        self.Saveas.setEnabled(True)
        # 打开文件为xml
        if fname.split('.')[-1] == 'xml':
            self.xmlpath = fname  # 打开的xml文件路径
            self.filekind = 1
            tree = ET.parse(fname)
            root = tree.getroot()

            # 读取图片路径将图片显示到label上
            imgpath = root.find('path').text
            self.filepath = imgpath
            self.centralWidget().imagelabel.setPixmap(QPixmap(imgpath))
            self.centralWidget().imagelabel.setScaledContents(True)
            self.imgwidth = self.centralWidget().imagelabel.width()
            self.imgheight = self.centralWidget().imagelabel.height()

            # 解析xml树，读取标注矩阵信息和标注内容
            for objectt in root.findall('object'):
                self.xmlrect = []  # 该列表存储单个矩阵的数据
                x = int(objectt.find('bndbox/xmin').text)
                y = int(objectt.find('bndbox/ymin').text)
                w = int(objectt.find('bndbox/xmax').text) - int(objectt.find('bndbox/xmin').text)
                h = int(objectt.find('bndbox/ymax').text) - int(objectt.find('bndbox/ymin').text)
                self.xmlrect.append(x)
                self.xmlrect.append(y)
                self.xmlrect.append(w)
                self.xmlrect.append(h)
                self.centralWidget().imagelabel.rects.append(self.xmlrect)  # 将单个矩阵信息通过循环加到总矩阵列表中
                name = objectt.find('name').text
                self.centralWidget().names.append(name)
            self.origtext = self.centralWidget().names[:]  # 保存原始数据，退出时判断是否修改
            self.origrect = self.centralWidget().imagelabel.rects[:]
            for i in range(0, len(self.centralWidget().names)):
                self.centralWidget().textlabels[i].setText(self.centralWidget().names[i])
                self.centralWidget().textlabels[i].setFont(QFont("e", 10))  # 设置字体的大小
                self.centralWidget().textlabels[i].setStyleSheet('''QWidget{background-color:rgb(240, 240, 240);}''')

        # 打开文件为图片
        else:
            self.filepath = fname
            image = QImage(fname)
            self.centralWidget().imagelabel.setPixmap(QPixmap.fromImage(image))
            self.centralWidget().imagelabel.adjustSize()
            self.centralWidget().imagelabel.setScaledContents(True)
            self.imgwidth = self.centralWidget().imagelabel.pixmap().width()
            self.imgheight = self.centralWidget().imagelabel.pixmap().height()

    # 使用截图功能
    def imagecut(self):
        if self.centralWidget().imagelabel.i == 24:
            self.edit.setDisabled(True)
            self.Create.setDisabled(True)
        self.Cutflag = True
        self.centralWidget().imagelabel.cutflag = self.Cutflag

    # 放大图像
    def zoominn(self):
        self.scaleIamge(1.2)

        """
        self.centralWidget().imagelabel.setPixmap(QPixmap(""))
        self.centralWidget().imagelabel.repaint()
        scale = 0.8
        img = QImage(self.filepath)
        owidth, oheight = img.size()
        print('o')
        mgnWidth = int(owidth * scale)
        mgnHeight = int(oheight * scale)  # 缩放宽高尺寸
        size = QSize(mgnWidth, mgnHeight)
        pixImg = QPixmap.fromImage(img.scaled(size, Qt.IgnoreAspectRatio))  # 修改图片实例大小并从QImage实例中生成QPixmap实例以备放入QLabel控件中
        print('y')
        self.centralWidget().imageLabel.setPixmap(pixImg)
        self.centralWidget().imagelabel.repaint()
        """

    # 缩小图像
    def zoomoutt(self):
        self.scaleIamge(0.8)
        # self.centralWidget().imagelabel.setPixmap(QPixmap(""))
        # self.centralWidget().imagelabel.repaint()

    def fitwin(self):
        self.centralWidget().imagelabel.move(0, 0)
        self.centralWidget().imagelabel.resize(int(5 * self.centralWidget().width() / 6), self.centralWidget().height())
        self.zoomin.setDisabled(True)
        self.zoomout.setDisabled(True)
        self.zoomi.setDisabled(True)
        self.zoomou.setDisabled(True)

    def fitnorm(self):
        self.centralWidget().imagelabel.move(int(5 * self.centralWidget().width() / 12 - self.imgwidth / 2),
                                             int(self.centralWidget().height() / 2 - self.imgheight / 2))
        self.scaleIamge(1.0)
        self.centralWidget().imagelabel.resize(self.imgwidth,self.imgheight)
        self.centralWidget().imagelabel.setScaledContents(True)

    # 调整图片大小
    def scaleIamge(self, factor):
        self.scaleFactor *= factor
        self.centralWidget().imagelabel.resize(self.scaleFactor * self.centralWidget().imagelabel.pixmap().size())
        # self.centralWidget().imagelabel.adjustSize()
        self.centralWidget().imagelabel.setScaledContents(True)
        self.zoomin.setEnabled(self.scaleFactor < 3.0)
        self.zoomout.setEnabled(self.scaleFactor > 0.25)
        self.zoomi.setEnabled(self.scaleFactor < 3.0)
        self.zoomou.setEnabled(self.scaleFactor > 0.25)

    def openhelp(self):
        inf = '可通过工具栏第三个按钮及菜单栏和编辑绘制矩形框绘制矩形框.\n右键单击矩形框或左键双击标注区标签可对标注内容进行修改.\n左键单击矩形框两边的点并移动可以拖动矩形框，拖动矩形框四角点可进行缩放.'

        QMessageBox.information(self, '说明', inf, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    """
    def view(self):
        for biaozhu in MyLabel().texts:
            self.textedit.setText(biaozhu)
   """
    # 使窗口居中
    def center(self):
        screen = QDesktopWidget().screenGeometry()  # 得到屏幕坐标
        size = self.geometry()  # 获取窗口坐标
        nem_left = (screen.width() - size.width()) / 2
        new_top = (screen.height() - size.height()) / 2
        self.move(int(nem_left), int(new_top - 100))

    # 构建添加子树
    def subElement(self, root, tag, text):
        ele = ET.SubElement(root, tag)
        ele.text = text
        ele.tail = '\n'

    # 保存构架xml文件
    def buildxml(self):
        # 修改原始数据
        self.origtext = self.centralWidget().names[:]
        self.origrect = self.centralWidget().imagelabel.rects[:]

        sender = self.sender()
        if sender == self.Saveas:
            self.filekind = 0
        if self.filekind == 0:
            defaultname = self.filepath.split('/')[-1].split('.')[0]  # 默认文件名
            #  print(self.filepath)
            #  print(defaultname)
            dirpath,dirtype = QFileDialog.getSaveFileName(self, '选择保存路径', defaultname, 'xml(*.xml)')  # 默认文件名为图片名称
            if not dirtype:
                return   # 防止取消退出

        # 构建文件xml树
        tree = ET.parse('ex.xml')
        root = tree.getroot()
        # 修改文件名
        sub1 = root.find('filename')
        # sub1.text = filename   # 汉字会有乱码，更换为baogangimg
        sub1.text = self.filepath.split('/')[-1]
        # 修改文件夹名
        sub1 = root.find('folder')
        sub1.text = self.filepath.split('/')[-2]
        # 修改文件路径
        sub1 = root.find('path')
        sub1.text = self.filepath

        img = Image.open(self.filepath, mode='r')
        # 获取图片的宽度和高度
        self.width, self.height = img.size
        channel = len(img.mode)
        # 修改宽度
        sub1 = root.find('size/width')
        sub1.text = str(self.width)
        # 修改高度
        sub1 = root.find('size/height')
        sub1.text = str(self.height)
        # 修改通道
        sub1 = root.find('size/depth')
        sub1.text = str(channel)

        # 根据标注列表长度循环构建xml子树
        i = len(self.centralWidget().imagelabel.rects)
        for j in range(0, i):
            objectt = ET.SubElement(root, 'object')  # 根节点子节点object
            croot = objectt

            # 解析图片长宽并判断是否截断
            x = self.centralWidget().imagelabel.rects[j][0]
            y = self.centralWidget().imagelabel.rects[j][1]
            x_max = self.centralWidget().imagelabel.rects[j][2] + self.centralWidget().imagelabel.rects[j][0]
            y_max = self.centralWidget().imagelabel.rects[j][1] + self.centralWidget().imagelabel.rects[j][3]
            if x == 0 or y == 0 or x_max == self.width or y_max == self.height:
                truncated = '1'
            else:
                truncated = '0'
            self.subElement(croot, "name", self.centralWidget().names[j])
            self.subElement(croot, "pose", "Unspecified")
            self.subElement(croot, "truncated", truncated)
            self.subElement(croot, "difficult", 0)

            bndbox = ET.SubElement(objectt, 'bndbox')  # object子节点bndbox
            ccroot = bndbox

            self.subElement(ccroot, "xmin", str(x))
            self.subElement(ccroot, "ymin", str(y))
            self.subElement(ccroot, "xmax", str(x_max))
            self.subElement(ccroot, "ymax", str(y_max))

        # 构建新树
        tree = ET.ElementTree(root)
        if self.filekind == 1:  # 再次保存
            tree.write(self.xmlpath, encoding="utf-8", xml_declaration=True)
        else:  # 第一次保存或另存
            tree.write(dirpath, encoding="utf-8", xml_declaration=True)
            # print('d')
            self.filekind = 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.setWindowIcon(QIcon('./resource/Kamen Rider 1 new.ico'))
    main.center()  # 窗口居中
    # main.showFullScreen()

    main.show()
    sys.exit(app.exec_())
