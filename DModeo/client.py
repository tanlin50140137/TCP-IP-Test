import socket

"""
socket协议
"""


class tcpClient:
    def __init__(self, host="127.0.0.1", port=80):
        self.isTcpClient = False
        try:
            self.sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sck.connect((host, port))
            self.isTcpClient = True
        except:
            self.isTcpClient = False

    def tcpReceive(self):
        return self.sck.recv(1024)

    def tcpSend(self, cmd):
        # self.sck.send(cmd.encode())
        self.sck.send(cmd)

    def tcpClose(self):
        self.sck.close()


# if __name__ == '__main__':
#     tcp = tcpClient("127.0.0.1", 9515)
#     tcp.tcpSend("A000050401008B")
#     while True:
#         data = tcp.tcpReceive()
#         if data != "":
#             print(data)
#     tcp.tcpClose()