import datetime
import os
import shutil
import sys
import shelve

from system_hotkey import SystemHotkey
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, pyqtSignal, QRect, QTimer, Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon, QPainter
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QListWidgetItem, \
    QFrame, QMessageBox, QFileDialog, QInputDialog, QLineEdit

from UI_EldenRingSaveCfg import Ui_MainWindow

_SAVE_DIR = os.path.join(os.path.expanduser('~'), r"AppData\Roaming\EldenRing")
_BACKUP_DIR = r"C:\EldenRingBackUp"


class Label2(QLabel):
    def __init__(self, parent=None):
        super(Label2, self).__init__(parent)

        self.setFixedWidth(340)

        self.text_rect = QRect(0, 0, 0, 0)
        self.start_pos = 0
        self.text_changed = True

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pos)
        self.timer.start(250)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setFont(QFont("Arial", 11, QFont.Bold))

        if self.text_rect.width() > self.width() and self.text_changed:
            painter.drawText(QRect(self.start_pos, 0, self.text_rect.width(), self.height()), Qt.AlignLeft | Qt.AlignVCenter, self.text())
        else:
            self.text_rect = painter.drawText(QRect(0, 0, self.width(), self.height()), Qt.AlignLeft | Qt.AlignVCenter, self.text())
            self.text_changed = True

    def update_pos(self):
        if (self.text_rect.width() + self.start_pos) > self.width():
            self.start_pos = self.start_pos - 5
        else:
            self.start_pos = 10

        self.update()

    # 备用函数，为后续不重建列表时，更新标题效果预留
    def on_text_changed(self):
        self.text_changed = False
        self.update()


class MyLabel(QWidget):
    # 删除信号
    deleted = pyqtSignal()
    # 重命名信号
    renamed = pyqtSignal()

    def __init__(self, title):
        super(MyLabel, self).__init__()

        self.lb_icon = QLabel()
        self.lb_icon.setFixedSize(26, 26)
        icon = QPixmap(":/icon/Elden.png").scaled(self.lb_icon.width(), self.lb_icon.height())
        self.lb_icon.setPixmap(icon)

        self.lb_title = Label2(title)
        self.line = QFrame()
        self.line.setFrameShape(QFrame.VLine)
        self.lb_recovery = QPushButton("恢复")
        self.lb_recovery.setFont(QFont("Arial", 11, QFont.Bold))
        self.lb_delete = QPushButton("删除")
        self.lb_delete.setFont(QFont("Arial", 11, QFont.Bold))
        self.lb_rename = QPushButton("重命名")
        self.lb_rename.setFont(QFont("Arial", 11, QFont.Bold))

        self.lb_main = QHBoxLayout()
        self.lb_main.addWidget(self.lb_icon)
        self.lb_main.addWidget(self.lb_title)
        self.lb_main.addWidget(self.line)
        self.lb_main.addWidget(self.lb_recovery)
        self.lb_main.addWidget(self.lb_delete)
        self.lb_main.addWidget(self.lb_rename)
        self.lb_main.setStretch(0, 7)
        self.lb_main.setStretch(3, 1)
        self.lb_main.setStretch(4, 1)
        self.lb_main.setStretch(5, 1)

        self.setLayout(self.lb_main)

        self.lb_recovery.clicked.connect(self.recovery)
        self.lb_delete.clicked.connect(self.delete)
        self.lb_rename.clicked.connect(self.rename)

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
                self.deleted.emit() # 此处暂时采用刷新方式
            except Exception as err:
                QMessageBox.warning(self, '警告', "删除当前备份失败！" + str(err), QMessageBox.Ok, QMessageBox.Ok)
                return

    def rename(self):
        text, okPressed = QInputDialog.getText(self, "重命名", "请输入新的文件名：", QLineEdit.Normal, self.lb_title.text())
        if okPressed and text != '':
            try:
                shutil.move(os.path.join(_BACKUP_DIR, self.lb_title.text()), os.path.join(_BACKUP_DIR, text))
                self.renamed.emit()
            except Exception as err:
                QMessageBox.warning(self, '警告', "重命名备份文件失败！" + str(err), QMessageBox.Ok, QMessageBox.Ok)
                return

class EldenRingSaveCfg(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(EldenRingSaveCfg, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())

        self.label_config.setFixedSize(19, 19)
        icon = QPixmap(":/icon/Config.png").scaled(self.label_config.width(), self.label_config.height())
        self.label_config.setIcon(QIcon(icon))

        self.pushButton.clicked.connect(self.backup)
        self.pushButton_3.clicked.connect(self.open_save_dir)
        self.pushButton_2.clicked.connect(self.open_backup_dir)
        self.pushButton_4.clicked.connect(self.refresh)
        self.label_config.clicked.connect(self.config_backup_dir)

        SystemHotkey().register(("f11",), callback=lambda x: self.pushButton.clicked.emit())

        _config_file_dir = os.path.join(os.path.expanduser('~'), r"AppData\Roaming\EldenRingBackUpConfig")
        if os.path.exists(_config_file_dir):
            try:
                global _BACKUP_DIR

                config_file = shelve.open(os.path.join(_config_file_dir, "Config"))
                _BACKUP_DIR = config_file["backup_dir"]
                config_file.close()
            except Exception as err:
                QMessageBox.warning(self, '警告', "读取备份位置失败，将使用默认位置备份！" + str(err), QMessageBox.Ok, QMessageBox.Ok)

        if not os.path.exists(_BACKUP_DIR):
            try:
                os.makedirs(_BACKUP_DIR)
            except Exception as err:
                QMessageBox.warning(self, '警告', "创建备份目录失败！" + str(err), QMessageBox.Ok, QMessageBox.Ok)
                return

        for saved in reversed(os.listdir(_BACKUP_DIR)):
            item_widget = QListWidgetItem()
            item_widget.setSizeHint(QSize(300, 44))
            self.listWidget.addItem(item_widget)

            label = MyLabel(saved)
            label.deleted.connect(self.refresh)
            label.renamed.connect(self.refresh)
            self.listWidget.setItemWidget(item_widget, label)

    def open_save_dir(self):
        try:
            os.startfile(_SAVE_DIR)
        except Exception as err:
            QMessageBox.warning(self, '警告', str(err), QMessageBox.Ok, QMessageBox.Ok)
            return

    def open_backup_dir(self):
        try:
            os.startfile(_BACKUP_DIR)
        except Exception as err:
            QMessageBox.warning(self, '警告', str(err), QMessageBox.Ok, QMessageBox.Ok)
            return

    def config_backup_dir(self):
        _config_file_dir = os.path.join(os.path.expanduser('~'), r"AppData\Roaming\EldenRingBackUpConfig")
        if not os.path.exists(_config_file_dir):
            try:
                os.makedirs(_config_file_dir)
            except Exception as err:
                QMessageBox.warning(self, '警告', "无法创建自定义文件，将使用默认配置！" + str(err), QMessageBox.Ok, QMessageBox.Ok)
                return

        global _BACKUP_DIR
        dir = QFileDialog.getExistingDirectory(self, "请选择备份文件夹位置", _BACKUP_DIR)
        if not dir:
            return
        if os.path.samefile(dir, _SAVE_DIR):
            QMessageBox.warning(self, '警告', "与存档位置重叠，不允许在此处备份！", QMessageBox.Ok, QMessageBox.Ok)
            return

        try:
            config_file = shelve.open(os.path.join(_config_file_dir, "Config"))
            config_file["backup_dir"] = dir
            config_file.close()
        except Exception as err:
            QMessageBox.warning(self, '警告', "无法创建自定义文件，将使用默认配置！" + str(err), QMessageBox.Ok, QMessageBox.Ok)
            return

        result = QMessageBox.question(self, '提示', "是否拷贝旧存档至当前位置，并删除旧的备份文件夹？", QMessageBox.Yes | QMessageBox.No,
                                      QMessageBox.No)
        if result == QMessageBox.No:
            _BACKUP_DIR = dir
            self.refresh()
            return

        try:
            for backuped in os.listdir(_BACKUP_DIR):
                shutil.copytree(os.path.join(_BACKUP_DIR, backuped), os.path.join(dir, backuped))
        except Exception as err:
            QMessageBox.warning(self, '警告', "拷贝旧存档失败！" + str(err), QMessageBox.Ok, QMessageBox.Ok)
            _BACKUP_DIR = dir
            self.refresh()
            return

        try:
            shutil.rmtree(_BACKUP_DIR)
        except Exception as err:
            QMessageBox.warning(self, '警告', "删除旧存档失败！" + str(err), QMessageBox.Ok, QMessageBox.Ok)
            _BACKUP_DIR = dir
            return

        _BACKUP_DIR = dir
        self.refresh()

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
        label.renamed.connect(self.refresh)
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
            label.renamed.connect(self.refresh)
            self.listWidget.setItemWidget(item_widget, label)


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    EldenRing = EldenRingSaveCfg()
    EldenRing.show()
    sys.exit(app.exec_())
