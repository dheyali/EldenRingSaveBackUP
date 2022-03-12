import datetime
import os
import shutil
import sys

from system_hotkey import SystemHotkey
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QListWidgetItem, \
    QFrame, QMessageBox

from UI_EldenRingSaveCfg import Ui_MainWindow

_SAVE_DIR = os.path.join(os.path.expanduser('~'), "AppData\Roaming\EldenRing")
_BACKUP_DIR = r"C:\EldenRingBackUp"


class MyLabel(QWidget):
    # 删除信号
    deleted = pyqtSignal()

    def __init__(self, title):
        super(MyLabel, self).__init__()

        self.lb_icon = QLabel()
        self.lb_icon.setFixedSize(26, 26)
        icon = QPixmap(":/icon/Elden.png").scaled(self.lb_icon.width(), self.lb_icon.height())
        self.lb_icon.setPixmap(icon)

        self.lb_title = QLabel(title)
        self.lb_title.setFont(QFont("Arial", 11, QFont.Bold))
        self.line = QFrame()
        self.line.setFrameShape(QFrame.VLine)
        self.lb_recovery = QPushButton("恢复")
        self.lb_recovery.setFont(QFont("Arial", 11, QFont.Bold))
        self.lb_delete = QPushButton("删除")
        self.lb_delete.setFont(QFont("Arial", 11, QFont.Bold))

        self.lb_main = QHBoxLayout()
        self.lb_main.addWidget(self.lb_icon)
        self.lb_main.addWidget(self.lb_title)
        self.lb_main.addWidget(self.line)
        self.lb_main.addWidget(self.lb_recovery)
        self.lb_main.addWidget(self.lb_delete)
        self.lb_main.setStretch(0, 6)
        self.lb_main.setStretch(3, 1)
        self.lb_main.setStretch(4, 1)

        self.setLayout(self.lb_main)

        self.lb_recovery.clicked.connect(self.recovery)
        self.lb_delete.clicked.connect(self.delete)

    def recovery(self):
        result = QMessageBox.warning(self, '警告', "是否确认恢复？这将覆盖当前存档！", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == QMessageBox.No:
            return
        else:
            try:
                shutil.rmtree(_SAVE_DIR)
            except Exception as err:
                QMessageBox.warning(self, '警告', "删除当前存档失败！" + str(err), QMessageBox.Ok, QMessageBox.Ok)
                if os.path.exists(_SAVE_DIR):
                    return
                QMessageBox.information(self, '说明', "直接使用备份创建新存档！", QMessageBox.Ok, QMessageBox.Ok)

            try:
                shutil.copytree(os.path.join(_BACKUP_DIR, self.lb_title.text()), _SAVE_DIR)
            except Exception as err:
                QMessageBox.warning(self, '警告', "恢复存档失败！" + str(err), QMessageBox.Ok, QMessageBox.Ok)
                return

    def delete(self):
        result = QMessageBox.warning(self, '警告', "是否确认删除此备份？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == QMessageBox.No:
            return
        else:
            try:
                shutil.rmtree(os.path.join(_BACKUP_DIR, self.lb_title.text()))
                self.deleted.emit()
            except Exception as err:
                QMessageBox.warning(self, '警告', "删除当前备份失败！" + str(err), QMessageBox.Ok, QMessageBox.Ok)


class EldenRingSaveCfg(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(EldenRingSaveCfg, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(560, 350)

        self.pushButton.clicked.connect(self.backup)
        self.pushButton_3.clicked.connect(self.open_save_dir)
        self.pushButton_2.clicked.connect(self.open_backup_dir)
        self.pushButton_4.clicked.connect(self.refresh)

        SystemHotkey().register(("f11",), callback=lambda x: self.pushButton.clicked.emit())

        if not os.path.exists(_BACKUP_DIR):
            try:
                os.makedirs(_BACKUP_DIR)
            except Exception as err:
                QMessageBox.warning(self, '警告', str(err), QMessageBox.Ok, QMessageBox.Ok)

        for saved in reversed(os.listdir(_BACKUP_DIR)):
            item_widget = QListWidgetItem()
            item_widget.setSizeHint(QSize(300, 44))
            self.listWidget.addItem(item_widget)

            label = MyLabel(saved)
            label.deleted.connect(self.refresh)
            self.listWidget.setItemWidget(item_widget, label)

    def open_save_dir(self):
        try:
            os.startfile(_SAVE_DIR)
        except Exception as err:
            QMessageBox.warning(self, '警告', str(err), QMessageBox.Ok, QMessageBox.Ok)

    def open_backup_dir(self):
        try:
            os.startfile(_BACKUP_DIR)
        except Exception as err:
            QMessageBox.warning(self, '警告', str(err), QMessageBox.Ok, QMessageBox.Ok)

    def backup(self):
        try:
            folderName = "EldenRingSave " + datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S')
            shutil.copytree(_SAVE_DIR, os.path.join(_BACKUP_DIR, folderName))
        except Exception as err:
            QMessageBox.warning(self, '警告', str(err), QMessageBox.Ok, QMessageBox.Ok)
            return

        item_widget = QListWidgetItem()
        item_widget.setSizeHint(QSize(300, 44))
        self.listWidget.insertItem(0, item_widget)

        label = MyLabel(folderName)
        label.deleted.connect(self.refresh)
        self.listWidget.setItemWidget(item_widget, label)

    def refresh(self):
        if not os.path.exists(_BACKUP_DIR):
            QMessageBox.warning(self, '警告', "备份目录不存在！", QMessageBox.Ok, QMessageBox.Ok)
            return

        self.listWidget.clear()

        for saved in reversed(os.listdir(_BACKUP_DIR)):
            item_widget = QListWidgetItem()
            item_widget.setSizeHint(QSize(300, 44))
            self.listWidget.addItem(item_widget)

            label = MyLabel(saved)
            label.deleted.connect(self.refresh)
            self.listWidget.setItemWidget(item_widget, label)


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    EldenRing = EldenRingSaveCfg()
    EldenRing.show()
    sys.exit(app.exec_())
