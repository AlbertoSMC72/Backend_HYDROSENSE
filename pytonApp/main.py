import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.setGeometry(200, 200, 300, 150)

        layout = QVBoxLayout()

        self.label_username = QLabel('Email:')
        self.lineEdit_username = QLineEdit()
        layout.addWidget(self.label_username)
        layout.addWidget(self.lineEdit_username)

        self.label_password = QLabel('Password:')
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.label_password)
        layout.addWidget(self.lineEdit_password)

        self.button_login = QPushButton('Login')
        self.button_login.clicked.connect(self.check_login)
        layout.addWidget(self.button_login)

        self.setLayout(layout)

    def check_login(self):
        email = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        
        url = 'http://54.242.46.13:3000/app/auth/login'
        payload = {
            'email': email,
            'password': password
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                QMessageBox.information(self, 'Login Successful', f"User: {data['user']}\nToken: {data['token']}\nRole: {data['rol']}")
            else:
                QMessageBox.warning(self, 'Login Failed', f"Error: {response.status_code}")
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"An error occurred: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
