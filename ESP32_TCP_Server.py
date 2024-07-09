import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import QRegExp
import socket
import struct

from_class = uic.loadUiType("/home/jinsa/TCP_Client.ui")[0]
class WindowClass(QMainWindow, from_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # print(self.findChild(QLineEdit, "portEdit"))
        # print(self.findChild(QPushButton, "ConnectBtn"))
        
        # ip address format
        range = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
        ipRegex = QRegExp("^" + range + "\\." + range + "\\." + \
                        range + "\\." + range + "$")

        self.ipEdit.setValidator(QRegExpValidator(ipRegex, self))
        self.portEdit.setValidator(QIntValidator())
        self.degree.setValidator(QIntValidator())
        
        self.setWindowTitle("TCP Client")
        
        
        self.ConnectBtn.clicked.connect(self.connect)
        self.DisconnectBtn.clicked.connect(self.disconnect)
        
        self.led21.clicked.connect(self.clickLED21)
        self.led22.clicked.connect(self.clickLED22)
        self.led23.clicked.connect(self.clickLED23)
    
    
        self.is_connected = True
        self.sock = None
    
    def clickLED21(self):
        isOn = self.led21.isChecked()
        self.updateLED(21, isOn)
        
    def clickLED22(self):
        isOn = self.led22.isChecked()
        self.updateLED(22, isOn)
        
    def clickLED23(self):
        isOn = self.led23.isChecked()
        self.updateLED(23, isOn)
        
    def updateLED(self, pin, status):
        
        data = struct.pack('@ii', pin, status)
        self.sock.send(data)
        test = struct.unpack('@ii', self.data)
        print(test)
        
            
        
    def __del__(self):
        if self.sock:
           self.sock.close()
        self.is_connected =False

    def connect(self):
        ip = self.ipEdit.text()
        port = self.portEdit.text()
        
        self.sock = socket.socket()
        self.sock.connect((ip, int(port)))
        
        self.foramt = struct.Struct('@ii')
        
        # message = "Hello TCP/IP!"
    

        # data=""
        
        # while len(data) < len(message):
        #     data += self.sock.recv(1).decode()
        
        # print(data)
        # self.sock.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_())