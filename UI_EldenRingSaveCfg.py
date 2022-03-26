# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_EldenRingSaveCfg.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(680, 350)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/Elden.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setFlat(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.label_config = QtWidgets.QPushButton(self.groupBox)
        self.label_config.setText("")
        self.label_config.setFlat(True)
        self.label_config.setObjectName("label_config")
        self.horizontalLayout_2.addWidget(self.label_config)
        self.verticalLayout.addWidget(self.groupBox)
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "EldenRing"))
        self.pushButton.setText(_translate("MainWindow", "备份"))
        self.pushButton_4.setText(_translate("MainWindow", "刷新列表"))
        self.pushButton_3.setText(_translate("MainWindow", "打开存档文件夹"))
        self.pushButton_2.setText(_translate("MainWindow", "打开备份文件夹"))
        self.label_config.setToolTip(_translate("MainWindow", "自定义备份位置"))
import Elden_rc
