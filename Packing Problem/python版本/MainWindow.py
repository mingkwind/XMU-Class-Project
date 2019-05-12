# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QPainter, QFont, QColor, QPen, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, \
     QPushButton, QSlider, QMessageBox,QLineEdit,QTextEdit
import sys
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1144, 700)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)#packing问题求解按钮
        self.pushButton.setGeometry(QtCore.QRect(455, 76, 151, 41))#求解按钮
        self.pushButton.setStyleSheet("font: 14pt \"Bahnschrift SemiLight\"")
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(980, 100, 141, 31))
        self.label.setStyleSheet("font: 16pt \"楷体\";")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1116, 140, 25, 16))
        self.label_2.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.label_2.setStyleSheet("font: 12pt \"Symbol\";")
        self.label_2.setObjectName("label_2")
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(980, 140, 131, 22))#演示速度
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(990, 170, 111, 41))#开始演示
        self.pushButton_2.setStyleSheet("font: 14pt \"Bahnschrift SemiLight\"")
        self.pushButton_2.setObjectName("pushButton_2")
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(192, 70, 42, 31))#样本个数
        self.spinBox.setStyleSheet("font: 16pt \"黑体\";")
        self.spinBox.setObjectName("spinBox")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)#字_样本个数
        self.label_3.setGeometry(QtCore.QRect(170, 15, 91, 31))
        self.label_3.setStyleSheet("font: 16pt \"楷体\";")
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(25, 70, 121, 31))#石砖长宽
        self.lineEdit.setStyleSheet("font: 12pt \"黑体\";")
        self.lineEdit.setObjectName("lineEdit")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)#字_石砖大小
        self.label_4.setGeometry(QtCore.QRect(40, 15, 91, 31))
        self.label_4.setStyleSheet("font: 16pt \"楷体\";")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)#字_样本大小
        self.label_5.setGeometry(QtCore.QRect(300,15, 91, 31))
        self.label_5.setStyleSheet("font: 16pt \"楷体\";")
        self.label_5.setObjectName("label_5")
        self.textEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(300, 50, 81, 85))#样本大小
        self.textEdit.setStyleSheet("font: 12pt \"黑体\";")
        self.textEdit.setObjectName("textEdit")
        self.label_6= QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(20, 140, 921, 511))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_6.setFont(font)
        self.label_6.setAutoFillBackground(True)
        self.label_6.setFrameShape(QtWidgets.QFrame.Box)
        self.label_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_6.setLineWidth(2)
        self.label_6.setScaledContents(True)  # 适应窗口
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(675,65, 131, 31))#字_最大利用率
        self.label_7.setStyleSheet("font: 16pt \"楷体\";")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)#最大利用率
        self.label_8.setGeometry(QtCore.QRect(800,65, 91, 31))
        self.label_8.setStyleSheet("font: 16pt \"楷体\";")
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)  # 显示方案
        self.label_9.setGeometry(QtCore.QRect(945,220, 190, 290))
        self.label_9.setStyleSheet("font: 16pt \"楷体\";")
        self.label_9.setObjectName("label_9")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(487, 35, 90, 28))
        self.comboBox.setStyleSheet("font: 75 italic 14pt \"Bodoni MT\";\n"
"color:rgb(0, 0, 255);")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(['0','1'])
        self.spinBox.raise_()
        self.pushButton.raise_()
        self.label.raise_()
        self.label_2.raise_()
        #self.graphicsView.raise_()
        self.horizontalSlider.raise_()
        self.pushButton_2.raise_()
        self.label_3.raise_()
        self.lineEdit.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.textEdit.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1144, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "小明的第一个程序"))
        self.pushButton.setText(_translate("MainWindow", "Packing问题求解"))
        self.label.setText(_translate("MainWindow", "选择演示速度"))
        self.label_2.setText(_translate("MainWindow", "10"))
        self.pushButton_2.setText(_translate("MainWindow", "开始演示"))
        self.label_3.setText(_translate("MainWindow", "样本个数"))
        self.lineEdit.setPlaceholderText("请输入长和宽！")
        self.lineEdit.setFocus()
        self.label_4.setText(_translate("MainWindow", "石砖大小"))
        self.label_5.setText(_translate("MainWindow", "样本大小"))
        self.label_7.setText(_translate("MainWindow", "最大利用率"))
        self.label_8.setText(_translate("MainWindow", "0.0%"))
        self.textEdit.setPlaceholderText("请输入\n各个样本\n长和宽！")
        self.comboBox.setItemText(0, _translate("MainWindow", "Rep"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Not Rep"))
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
