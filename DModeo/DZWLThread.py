import serial
from PyQt5.QtCore import *
from DModeo.client import tcpClient

"""
线程处理
"""


# 串口
class SerialThread(QThread):
    """
    # 更多示例
    # self.main_engine.write(chr(0x06).encode("utf-8"))  # 十六制发送一个数据
    # print(self.main_engine.read().hex())  # 十六进制的读取读一个字节
    # print(self.main_engine.read())  # 读一个字节
    # print(self.main_engine.read(10).decode("gbk"))  # 读十个字节
    # print(self.main_engine.readline().decode("gbk"))  # 读一行
    # print(self.main_engine.readlines())  # 读取多行，返回列表，必须匹配超时（timeout)使用
    # print(self.main_engine.in_waiting)  # 获取输入缓冲区的剩余字节数
    # print(self.main_engine.out_waiting)  # 获取输出缓冲区的字节数
    # print(self.main_engine.readall())  # 读取全部字符。
    """
    SerialReceiveSignal = pyqtSignal(dict)

    def __init__(self, port: str, bps: int, timeout: float):
        super(SerialThread, self).__init__()
        self.stop = False
        self.isOpen = False
        self.port = port
        try:
            # 打开串口，并得到串口对象
            self.main_engine = serial.Serial(port, bps, timeout=timeout)
            # 判断是否打开成功
            if self.main_engine.is_open:
                self.isOpen = True
        except Exception as err:
            print(err)

    # 停止线程
    def setStop(self, b):
        self.stop = b

    # 发送数据
    def send(self, cmd, flag=0):
        try:
            if flag == 0:
                # 发送文本模式
                data = bytes(cmd, encoding='utf-8')
                self.main_engine.write(data)
            else:
                # 发送HEX模式
                if len(cmd) % 2 == 0:
                    data = bytes.fromhex(cmd)
                    self.main_engine.write(data)
                else:
                    self.SerialReceiveSignal.emit({"ret": f"发送HEX模式的个数‘{cmd}‘应为2的整数倍", "mode": 0})

        except Exception as err:
            self.SerialReceiveSignal.emit({"ret": f"发送数据, 异常{err}", "mode": 0})

    # 接收数据
    def run(self):
        try:
            back = f"<font color='#ff00ff'>设备名字:{self.main_engine.name}, 波特率:{self.main_engine.baudrate}, 校验位:{self.main_engine.parity}, 停止位:{self.main_engine.stopbits}</font>"
            self.SerialReceiveSignal.emit({"ret": f"{back}, 打开", "mode": 0})
            while True:
                if self.stop:
                    self.SerialReceiveSignal.emit({"ret": f"{back}, 关闭", "mode": 0})
                    break
                # 接收数据
                data = self.main_engine.readline()
                # 返回数据
                self.SerialReceiveSignal.emit({"ret": data, "mode": "data"})
            # 关闭串口
            self.main_engine.close()
        except Exception as err:
            self.SerialReceiveSignal.emit({"ret": f"接收数据, 异常{err}", "mode": 0})


# TCP
class TCPThread(QThread):
    """
    启用TCP
    """
    tcpReceiveSignal = pyqtSignal(dict)

    # 初始化
    def __init__(self, ip: str, port: int):
        super(TCPThread, self).__init__()
        self.stop = False
        self.isTCP = False
        try:
            self.tcp = tcpClient(ip, port)
            self.isTCP = self.tcp.isTcpClient
        except:
            self.isTCP = False
    # 停止线程
    def setStop(self, b):
        self.stop = b

    # 发送数据
    def send(self, cmd, flag=0):
        try:
            if flag == 0:
                # 发送文本模式
                data = bytes(cmd, encoding='utf-8')
                self.tcp.tcpSend(data)
            else:
                # 发送HEX模式
                if len(cmd) % 2 == 0:
                    data = bytes.fromhex(cmd)
                    self.tcp.tcpSend(data)
                else:
                    self.tcpReceiveSignal.emit({"ret": f"发送HEX模式的个数‘{cmd}‘应为2的整数倍", "mode": 0})
        except Exception as err:
            self.tcpReceiveSignal.emit({"ret": f"发送数据, 异常{err}", "mode": 0})

    # 接收数据
    def run(self):
        try:
            self.tcpReceiveSignal.emit({"ret": "TCP客户端打开", "mode": 0})
            while True:
                # 线程结束
                if self.stop:
                    self.tcpReceiveSignal.emit({"ret": "TCP客户端关闭", "mode": 0})
                    break
                # 接收数据
                data = self.tcp.tcpReceive()
                if not data:
                    break
                # 返回数据
                self.tcpReceiveSignal.emit({"ret": data, "mode": "data"})
            # 关闭TCP
            self.tcp.tcpClose()
        except Exception as err:
            self.tcpReceiveSignal.emit({"ret": f"接收数据, 异常{err}", "mode": 0})
