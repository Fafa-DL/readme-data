import sys
from PyQt5.QtWidgets import (QMainWindow,QMessageBox,QLineEdit,QApplication)
# from PyQt5.QtGui import *

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QCoreApplication

from Ui_login import Ui_Loginwindow
from GUI import MainWin
# 登陆对话框
class loginUI(QMainWindow,Ui_Loginwindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.initUI()
		
    def initUI(self):
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.pushButton.clicked.connect(self.btn_login_fuc)
        self.pushButton_2.clicked.connect(self.closewindow)

    def btn_login_fuc(self):
        #1 获取输入的账户和密码
        account = self.lineEdit.text()  # 记得text要打括号（）！
        password = self.lineEdit_2.text()
        if self.checkBox.isChecked():
            if account == "" or password == "":
                reply = QMessageBox.warning(self,"警告","账号密码不能为空，请输入！")
                return
            elif account == '啥都会一点的研究生' and password =='66668888':
                self.xx = MainWin()
                self.close()
            else:
                reply = QMessageBox.warning(self,"警告","账号或密码错误！")
        else:
            reply = QMessageBox.warning(self,"警告","没关注还想白嫖！")
            import webbrowser
            webbrowser.open('https://space.bilibili.com/46880349')
            self.close()
    def closewindow(self):
        self.close()
        
            
            
if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    d = loginUI()
    d.show()
    sys.exit(app.exec())