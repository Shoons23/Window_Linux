import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import QRegExp, QTimer
import socket
import struct
import datetime


from_class = uic.loadUiType("/home/jinsa/TCP_Client.ui")[0]
class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.connected = False
        
        # timer
        self.timer = QTimer(self)
        self.timer.start(100)
        # IP 주소 형식
        range = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
        ipRegex = QRegExp("^" + range + "\\." + range + "\\." + range + "\\." + range + "$")
        
        self.ipEdit.setValidator(QRegExpValidator(ipRegex, self))
        self.portEdit.setValidator(QIntValidator(1, 65535, self))  # 포트 범위: 1-65535
        self.degree.setValidator(QIntValidator())
        self.setWindowTitle("TCP Client")
        
        self.ConnectBtn.clicked.connect(self.connect)
        self.DisconnectBtn.clicked.connect(self.disconnect)
        
        self.led21.clicked.connect(self.clickLED21)
        self.led22.clicked.connect(self.clickLED22)
        self.led23.clicked.connect(self.clickLED23)
        self.moveBtn.clicked.connect(self.clickMove)
        self.timer.timeout.connect(self.timeout)
        
        self.sock = None  # 소켓을 초기화합니다
        self.is_connected = False  # 연결 상태를 추적하는 플래그
    
    def timeout(self):
        self.updateLED(35,0)
    
    def clickMove(self):
        degree = int(self.degree.text())
        self.updateLED(5, degree)
        
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
        if not self.is_connected or self.sock is None:
            QMessageBox.warning(self, "오류", "서버에 연결되지 않았습니다.")
            return
        try:
            data = struct.pack('@ii', pin, status)
            self.sock.send(data)
            test = struct.unpack('@ii', data)
            if test[0] == 35:
                self.sensor.setText(str(test[1]))
            print(test)
        except socket.error as e:
            QMessageBox.critical(self, "전송 오류", f"데이터 전송에 실패했습니다: {e}")
            self.disconnect()
    
    # def updateLED2(self, pin, status):
    #     if self.connected == True:
    #         data = self.format.pack(pin, status)
    #         req = self.sock.send(data)
    #         rev = self.format.unpack(self.sock.recv(self.format.size))
    #         if rev[0] == 35:
    #             self.sensor.setText(str(rev[1]))
                
    #         print(rev)
    


    def disconnect(self):
        if self.sock:
            try:
                self.sock.close()
                QMessageBox.information(self, "연결 상태", "연결이 해제되었습니다.")
            except socket.error as e:
                QMessageBox.critical(self, "해제 오류", f"연결 해제에 실패했습니다: {e}")
            finally:
                self.sock = None
                self.is_connected = False
        else:
            QMessageBox.warning(self, "오류", "연결이 되어 있지 않습니다.")

    def connect(self):
        ip = self.ipEdit.text()
        port = self.portEdit.text()
        
        if not ip or not port:
            QMessageBox.warning(self, "입력 오류", "IP 주소와 포트 번호를 모두 입력하세요.")
            return

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((ip, int(port)))
            self.is_connected = True
            QMessageBox.information(self, "연결 상태", "성공적으로 연결되었습니다.")
        except socket.error as e:
            QMessageBox.critical(self, "연결 오류", f"연결에 실패했습니다: {e}")
            self.sock = None
            self.is_connected = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_())
