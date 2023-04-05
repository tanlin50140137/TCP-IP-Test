import sys
import binascii
import time

import res
from DModeo.DZWLThread import *
from DModeo.MSGLayout import *
from DModeo.crc16 import *

"""
主窗口程序
pyrcc5 -o res.py res.qrc
pyinstaller -F -w -i ./logo.ico ./DZWL.py
"""


class MyMainWindow(QWidget):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.setWindowTitle("测试命令集")
        self.setWindowIcon(QIcon(":logo.ico"))
        self.resize(1400, 800)
        self.setMinimumSize(1400, 800)

        self.mlLineEdit = {}
        self.mlTextBrowser = {}
        self.index = 0
        self.selcetFlag = 0
        self.sendModeIndex = 0
        self.tabWidget = {}

        self.setUpInit()

    # 出始化控件
    def setUpInit(self):
        # 协议
        self.TcpComGroupBox = QGroupBox("协议")
        self.TcpRadioButton = QRadioButton("TCP/IP")
        self.TcpRadioButton.setChecked(True)
        self.TcpRadioButton.clicked.connect(self.TcpRadioButtonSlot)
        self.ComRadioButton = QRadioButton("串口")
        self.ComRadioButton.clicked.connect(self.TcpRadioButtonSlot)
        self.TcpComHBoxLayout = QHBoxLayout()
        self.TcpComHBoxLayout.addWidget(self.TcpRadioButton)
        self.TcpComHBoxLayout.addWidget(self.ComRadioButton)
        self.TcpComGroupBox.setLayout(self.TcpComHBoxLayout)
        # 链接TCP/IP
        self.TcpGroupBox = QGroupBox("TCP/IP 客户端")
        self.TcpLabel = QLabel("IP:")
        self.TcpEdit = QLineEdit()
        self.TcpEdit.setInputMask('000.000.000.000;')
        self.TcpEdit.setAlignment(Qt.AlignCenter)
        self.TcpEdit.setFixedWidth(160)
        self.TcpPortLabel = QLabel("端口:")
        self.TcpPortEdit = QLineEdit()
        self.TcpPortEdit.setAlignment(Qt.AlignCenter)
        self.TcpPortEdit.setFixedWidth(80)
        self.TcpOpenButton = QPushButton("打开")
        self.TcpOpenButton.clicked.connect(self.TcpOpenButtonSlot)
        self.TcpCloseButton = QPushButton("关闭")
        self.TcpCloseButton.clicked.connect(self.TcpCloseButtonSlot)
        self.TcpCloseButton.setEnabled(False)
        self.TcpHBoxLayout = QHBoxLayout()
        self.TcpHBoxLayout.addStretch(0)
        self.TcpHBoxLayout.addWidget(self.TcpLabel)
        self.TcpHBoxLayout.addWidget(self.TcpEdit)
        self.TcpHBoxLayout.addWidget(self.TcpPortLabel)
        self.TcpHBoxLayout.addWidget(self.TcpPortEdit)
        self.TcpHBoxLayout.addWidget(self.TcpOpenButton)
        self.TcpHBoxLayout.addWidget(self.TcpCloseButton)
        self.TcpHBoxLayout.addStretch(0)
        self.TcpGroupBox.setLayout(self.TcpHBoxLayout)
        # 串口
        self.ComGroupBox = QGroupBox("连接串口")
        self.ComGroupBox.setEnabled(False)
        self.ComComboBox = QComboBox()
        self.ComComboBox.addItem("COM1")
        self.ComComboBox.addItem("COM2")
        self.ComComboBox.addItem("COM3")
        self.ComComboBox.addItem("COM4")
        self.ComComboBox.addItem("COM5")
        self.ComComboBox.addItem("COM6")
        self.ComPortLabel = QLabel("波特率:")
        self.ComPortEdit = QLineEdit()
        self.ComPortEdit.setAlignment(Qt.AlignCenter)
        self.ComPortEdit.setFixedWidth(80)
        self.ComOpenButton = QPushButton("打开")
        self.ComOpenButton.clicked.connect(self.ComOpenButtonSlot)
        self.ComCloseButton = QPushButton("关闭")
        self.ComCloseButton.clicked.connect(self.ComCloseButtonSlot)
        self.ComCloseButton.setEnabled(False)
        self.ComHBoxLayout = QHBoxLayout()
        self.ComHBoxLayout.addStretch(0)
        self.ComHBoxLayout.addWidget(self.ComComboBox)
        self.ComHBoxLayout.addWidget(self.ComPortLabel)
        self.ComHBoxLayout.addWidget(self.ComPortEdit)
        self.ComHBoxLayout.addWidget(self.ComOpenButton)
        self.ComHBoxLayout.addWidget(self.ComCloseButton)
        self.ComHBoxLayout.addStretch(0)
        self.ComGroupBox.setLayout(self.ComHBoxLayout)
        # tcp服务端
        self.TcpServerGroupBox = QGroupBox("TCP/IP 服务端")
        self.TcpServerOpenButton = QPushButton("创建服务器")
        self.TcpServerOpenButton.clicked.connect(self.TcpServerOpenButtonSlot)
        self.TcpServerHBoxLayout = QHBoxLayout()
        self.TcpServerHBoxLayout.addWidget(self.TcpServerOpenButton)
        self.TcpServerGroupBox.setLayout(self.TcpServerHBoxLayout)
        # 上部份布局
        self.ttHBoxLayout = QHBoxLayout()
        self.ttHBoxLayout.addWidget(self.TcpComGroupBox)
        self.ttHBoxLayout.addWidget(self.TcpGroupBox)
        self.ttHBoxLayout.addWidget(self.ComGroupBox)
        self.ttHBoxLayout.addStretch(0)
        self.ttHBoxLayout.addWidget(self.TcpServerGroupBox)
        # 选项卡
        self.TabWidget = QTabWidget()
        self.TabWidget.currentChanged.connect(self.TabWidgetSlot)
        self.Tab1 = QWidget()
        self.Tab2 = QWidget()
        self.TabWidget.addTab(self.Tab1, "硬件指令集操作")
        self.TabWidget.addTab(self.Tab2, "写卡指令集操作")
        # 初始化选项卡
        self.Tab1Init()
        self.Tab2Init()
        # 窗口布局
        self.WindowsVBoxLayout = QVBoxLayout()
        self.WindowsVBoxLayout.addLayout(self.ttHBoxLayout)
        self.WindowsVBoxLayout.addWidget(self.TabWidget)
        self.setLayout(self.WindowsVBoxLayout)

    # 创建TCP服务端
    def TcpServerOpenButtonSlot(self):
        index = self.TabWidget.count()
        self.tabWidget[index] = QWidget()

        self.TabWidget.insertTab(index, self.tabWidget[index], "新TCP")

    # 选项卡槽
    def TabWidgetSlot(self, i):
        self.index = i

    # 发送命令
    def sendPushButtonSlot(self):
        cmd = self.mlLineEdit[self.index].text()
        if cmd == "":
            if self.index == 0:
                return Tip.AskMsg("提示", "你还没有输入硬件指令，无法发送", "我知道了")
            else:
                return Tip.AskMsg("提示", "你还没有输入写卡指令，无法发送", "我知道了")
        cmd = cmd.replace(' ', '').replace("　", '').replace("\n", '').replace("\t", '').replace("\s", '')
        # 发送时间　
        self.mlTextBrowser[self.index].append(f"<font color='#0000FF'><b>发送：{cmd}　<font color='#999999'>时间：{time.strftime('%Y/%m/%d %H:%M:%S')}</font></b></font>")
        try:
            if self.selcetFlag == 0:
                # TCP
                self.tcpip.send(cmd, self.sendModeIndex)
            else:
                # 串口
                self.serialThread.send(cmd, self.sendModeIndex)
        except Exception as err:
            # 提示错误
            file = err.__traceback__.tb_frame.f_globals["__file__"]
            line = err.__traceback__.tb_lineno
            self.mlTextBrowser[self.index].append(f"<font color='red'>Exception(\n\t{file}\n\t{err} in line {line}\n)</font>")

    # 清空
    def clearPushButtonSlot(self):
        self.mlTextBrowser[self.index].clear()

    # Tcp接收数据返回槽
    def tcpReceiveSlot(self, dit):
        if len(dit['ret']) > 0:
            # 解析文本模式
            if dit['mode'] == 'data':
                # 服务器数据
                if self.sendModeIndex == 0:
                    ret = dit['ret'].decode('UTF-8')
                else:
                    ret = binascii.b2a_hex(dit['ret']).decode('UTF-8')
            # 错误提示
            else:
                ret = dit['ret']
            # 显示数据
            self.mlTextBrowser[self.index].append(f"<font color='#333333'><b>接收：{ret}</b></font>")

    # 选项卡1
    def Tab1Init(self):
        mlGroupBox = QGroupBox("指令集操作")
        mlLabel = QLabel("输入指令：")
        self.mlLineEdit[0] = QLineEdit()
        self.sendMode1 = QComboBox()
        self.sendMode1.addItem("文本模式")
        self.sendMode1.addItem("HEX模式")
        self.sendMode1.currentIndexChanged.connect(self.sendModeSlot)
        sendPushButton = QPushButton("发送")
        sendPushButton.clicked.connect(self.sendPushButtonSlot)
        mlHBoxLayout = QHBoxLayout()
        mlHBoxLayout.addWidget(mlLabel)
        mlHBoxLayout.addWidget(self.sendMode1)
        mlHBoxLayout.addWidget(self.mlLineEdit[0])
        mlHBoxLayout.addWidget(sendPushButton)
        mlGroupBox.setLayout(mlHBoxLayout)
        # 返回内容
        self.mlTextBrowser[0] = QTextBrowser()
        self.mlTextBrowser[0].document().setMaximumBlockCount(100)
        # 清空显示区
        clearPushButton = QPushButton("清空")
        clearPushButton.clicked.connect(self.clearPushButtonSlot)
        clHBoxLayout = QHBoxLayout()
        clHBoxLayout.addStretch(0)
        clHBoxLayout.addWidget(clearPushButton)
        # 模板布局
        VBoxLayout = QVBoxLayout()
        VBoxLayout.addWidget(mlGroupBox)
        VBoxLayout.addWidget(self.mlTextBrowser[0])
        VBoxLayout.addLayout(clHBoxLayout)
        self.Tab1.setLayout(VBoxLayout)

    # 选项卡2
    def Tab2Init(self):
        mlGroupBox = QGroupBox("写卡指令集操作")
        mlLabel = QLabel("输入写卡指令：")
        self.mlLineEdit[1] = QLineEdit()
        self.sendMode2 = QComboBox()
        self.sendMode2.addItem("文本模式")
        self.sendMode2.addItem("HEX模式")
        self.sendMode2.currentIndexChanged.connect(self.sendModeSlot)
        sendPushButton= QPushButton("发送")
        sendPushButton.clicked.connect(self.sendPushButtonSlot)
        mlHBoxLayout = QHBoxLayout()
        mlHBoxLayout.addWidget(mlLabel)
        mlHBoxLayout.addWidget(self.sendMode2)
        mlHBoxLayout.addWidget(self.mlLineEdit[1])
        mlHBoxLayout.addWidget(sendPushButton)
        mlGroupBox.setLayout(mlHBoxLayout)
        # 返回内容
        self.mlTextBrowser[1] = QTextBrowser()
        self.mlTextBrowser[1].document().setMaximumBlockCount(100)
        # 清空显示区
        clearPushButton = QPushButton("清空")
        clearPushButton.clicked.connect(self.clearPushButtonSlot)
        clHBoxLayout = QHBoxLayout()
        clHBoxLayout.addStretch(0)
        clHBoxLayout.addWidget(clearPushButton)
        # 校验内容
        jyGroupBox = QGroupBox("CRC-16校验")
        self.jyLineEdit1 = QLineEdit()
        self.jyLineEdit2 = QLineEdit()
        self.jyLineEdit2.setAlignment(Qt.AlignCenter)
        self.jyLineEdit2.setFixedWidth(100)
        jyFormLayout = QFormLayout()
        jyFormLayout.addRow("校验内容：", self.jyLineEdit1)
        jyFormLayout.addRow("校验结果：", self.jyLineEdit2)
        jyPushButton = QPushButton("计算")
        jyPushButton.clicked.connect(self.jyPushButtonSlot)
        jyHBoxLayout = QHBoxLayout()
        jyHBoxLayout.addStretch(0)
        jyHBoxLayout.addWidget(jyPushButton)
        jyVBoxLayout = QVBoxLayout()
        jyVBoxLayout.addLayout(jyFormLayout)
        jyVBoxLayout.addLayout(jyHBoxLayout)
        jyGroupBox.setLayout(jyVBoxLayout)
        # 模板布局
        VBoxLayout = QVBoxLayout()
        VBoxLayout.addWidget(jyGroupBox)
        VBoxLayout.addWidget(mlGroupBox)
        VBoxLayout.addWidget(self.mlTextBrowser[1])
        VBoxLayout.addLayout(clHBoxLayout)
        self.Tab2.setLayout(VBoxLayout)

    # 发送模式
    def sendModeSlot(self, i):
        self.sendModeIndex = i
        # 设置下拉框
        self.sendMode1.setCurrentIndex(i)
        self.sendMode2.setCurrentIndex(i)

    # CRC-16校验
    def jyPushButtonSlot(self):
        val = self.jyLineEdit1.text()
        if val == "":
            return Tip.AskMsg("提示", "你还没有输入校验内容，无法计算", "我知道了")
        val = val.replace(' ', '').replace("　", '').replace("\n", '').replace("\t", '').replace("\s", '')
        a, b = calc_crc(val)
        self.jyLineEdit2.setText(f"{a} {b}")

    # 打开TCP
    def TcpOpenButtonSlot(self):
        ip = self.TcpEdit.text()
        if ip == '':
            return Tip.AskMsg("提示", "你还没有输入IP，无法打开", "我知道了")
        port = self.TcpPortEdit.text()
        if port == '':
            return Tip.AskMsg("提示", "你还没有输入端口，无法打开", "我知道了")
        port = int(port)
        try:
            self.tcpip = TCPThread(ip, port)
            self.tcpip.tcpReceiveSignal.connect(self.tcpReceiveSlot)
            self.tcpip.start()
            if self.tcpip.isTCP:
                # 按钮状态
                self.TcpOpenButton.setEnabled(False)
                self.TcpCloseButton.setEnabled(True)
        except Exception as err:
            # 按钮状态
            self.TcpOpenButton.setEnabled(True)
            self.TcpCloseButton.setEnabled(False)
            # 提示错误
            file = err.__traceback__.tb_frame.f_globals["__file__"]
            line = err.__traceback__.tb_lineno
            self.mlTextBrowser[self.index].append(f"<font color='red'>Exception(<br/>{file}<br/>Error：{err}，in line {line}<br/>)</font>")

    # 关闭TCP
    def TcpCloseButtonSlot(self):
        try:
            # 表示结束
            self.tcpip.setStop(True)
            self.tcpip.send(" ")
            # 按钮状态
            self.TcpOpenButton.setEnabled(True)
            self.TcpCloseButton.setEnabled(False)
        except Exception as err:
            # 按钮状态
            self.TcpOpenButton.setEnabled(True)
            self.TcpCloseButton.setEnabled(False)
            # 提示错误
            file = err.__traceback__.tb_frame.f_globals["__file__"]
            line = err.__traceback__.tb_lineno
            self.mlTextBrowser[self.index].append(f"<font color='red'>Exception(<br/>{file}<br/>Error：{err}，in line {line}<br/>)</font>")

    # 串口打开按钮
    def ComOpenButtonSlot(self):
        com = self.ComComboBox.currentText()
        bot = self.ComPortEdit.text()
        if bot == '':
            return Tip.AskMsg("提示", "你还没有输入波特率，无法打开", "我知道了")
        bot = int(bot)
        # 打开串口
        try:
            self.serialThread = SerialThread(com, bot, 0.5)
            self.serialThread.SerialReceiveSignal.connect(self.tcpReceiveSlot)
            self.serialThread.start()
            # 按钮状态
            if self.serialThread.isOpen:
                self.ComOpenButton.setEnabled(False)
                self.ComCloseButton.setEnabled(True)
        except Exception as err:
            # 按钮状态
            self.ComOpenButton.setEnabled(True)
            self.ComCloseButton.setEnabled(False)
            # 提示错误
            file = err.__traceback__.tb_frame.f_globals["__file__"]
            line = err.__traceback__.tb_lineno
            self.mlTextBrowser[self.index].append(f"<font color='red'>Exception(<br/>{file}<br/>Error：{err}，in line {line}<br/>)</font>")

    # 串口关闭按钮
    def ComCloseButtonSlot(self):
        try:
            # 表示结束
            self.serialThread.setStop(True)
            self.serialThread.send("<font color='#ff00ff'>00FF00FF00FF00FF, TCP关闭了</font>")
            # 按钮状态
            self.ComOpenButton.setEnabled(True)
            self.ComCloseButton.setEnabled(False)
        except Exception as err:
            # 按钮状态
            self.ComOpenButton.setEnabled(True)
            self.ComCloseButton.setEnabled(False)
            # 提示错误
            file = err.__traceback__.tb_frame.f_globals["__file__"]
            line = err.__traceback__.tb_lineno
            self.mlTextBrowser[self.index].append(f"<font color='red'>Exception(<br/>{file}<br/>Error：{err}，in line {line}<br/>)</font>")

    # 协议槽函数
    def TcpRadioButtonSlot(self):
        val = self.sender().text()
        if val == self.TcpRadioButton.text():
            # TCP/IP
            self.selcetFlag = 0
            self.ComGroupBox.setEnabled(False)
            self.TcpGroupBox.setEnabled(True)
            try:
                self.serialThread.setStop(True)
                # 按钮状态
                self.ComOpenButton.setEnabled(True)
                self.ComCloseButton.setEnabled(False)
            except:
                pass
        elif val == self.ComRadioButton.text():
            # 串口
            self.selcetFlag = 1
            self.TcpGroupBox.setEnabled(False)
            self.ComGroupBox.setEnabled(True)
            try:
                self.tcpip.setStop(True)
                self.tcpip.send(" ")
                # 按钮状态
                self.TcpOpenButton.setEnabled(True)
                self.TcpCloseButton.setEnabled(False)
            except:
                pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyMainWindow()
    win.show()
    sys.exit(app.exec_())