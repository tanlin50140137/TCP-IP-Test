from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

"""
提示层
"""


class Tip(QMessageBox):
    def __init__(self):
        super(Tip, self).__init__()

    # 询问框
    @staticmethod
    def InputAbout(title: str, msg: str, buttonY='yes', buttonN='no'):
        about = Tip()
        about.setWindowTitle(title)
        about.setWindowIcon(QIcon(":logo.ico"))
        about.setText(msg)
        about.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        about.buttonY = about.button(QMessageBox.Yes)
        about.buttonY.setText(buttonY)
        about.buttonN = about.button(QMessageBox.No)
        about.buttonN.setText(buttonN)
        about.exec_()

        if about.clickedButton() == about.buttonY:
            return True
        else:
            return False

    # 询问框
    @staticmethod
    def AskAbout(title: str, msg: str, buttonY='yes', buttonN='no'):
        about = Tip()
        about.setWindowTitle(title)
        about.setWindowIcon(QIcon(":logo.ico"))
        about.setText(msg)
        about.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        about.buttonY = about.button(QMessageBox.Yes)
        about.buttonY.setText(buttonY)
        about.buttonN = about.button(QMessageBox.No)
        about.buttonN.setText(buttonN)
        about.exec_()

        if about.clickedButton() == about.buttonY:
            return True
        else:
            return False

    # 提示
    @staticmethod
    def AskMsg(title: str, msg: str, buttonY='yes'):
        msgTip = Tip()
        msgTip.setWindowTitle(title)
        msgTip.setWindowIcon(QIcon(":logo.ico"))
        msgTip.setText(msg)
        msgTip.setStandardButtons(QMessageBox.Yes)
        msgTip.buttonY = msgTip.button(QMessageBox.Yes)
        msgTip.buttonY.setText(buttonY)
        msgTip.exec_()

        if msgTip.clickedButton() == msgTip.buttonY:
            return True
        else:
            return False
