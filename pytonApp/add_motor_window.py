import requests
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from session import Session

class AddMotorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Agregar Motor')
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        self.label_name = QLabel('Nombre:')
        self.lineEdit_name = QLineEdit()
        layout.addWidget(self.label_name)
        layout.addWidget(self.lineEdit_name)

        self.label_HP = QLabel('HP:')
        self.lineEdit_HP = QLineEdit()
        layout.addWidget(self.label_HP)
        layout.addWidget(self.lineEdit_HP)

        self.label_amperage = QLabel('Amperaje:')
        self.lineEdit_amperage = QLineEdit()
        layout.addWidget(self.label_amperage)
        layout.addWidget(self.lineEdit_amperage)

        self.label_voltage = QLabel('Voltaje:')
        self.lineEdit_voltage = QLineEdit()
        layout.addWidget(self.label_voltage)
        layout.addWidget(self.lineEdit_voltage)

        self.label_frequency = QLabel('Frecuencia:')
        self.lineEdit_frequency = QLineEdit()
        layout.addWidget(self.label_frequency)
        layout.addWidget(self.lineEdit_frequency)

        self.label_RPM = QLabel('RPM:')
        self.lineEdit_RPM = QLineEdit()
        layout.addWidget(self.label_RPM)
        layout.addWidget(self.lineEdit_RPM)

        self.button_submit = QPushButton('Crear Motor')
        self.button_submit.clicked.connect(self.submit_motor)
        layout.addWidget(self.button_submit)

        self.setLayout(layout)

    def submit_motor(self):
        name = self.lineEdit_name.text()
        HP = self.lineEdit_HP.text()
        amperage = self.lineEdit_amperage.text()
        voltage = self.lineEdit_voltage.text()
        frequency = self.lineEdit_frequency.text()
        RPM = self.lineEdit_RPM.text()
        
        session = Session()
        user_data = session.get_user_data()
        company_ref = user_data['user']
        
        url = 'http://3.234.90.94:3000/app/engine/'
        payload = {
            'name': name,
            'HP': float(HP),
            'amperage': float(amperage),
            'voltage': int(voltage),
            'frequency': int(frequency),
            'RPM': int(RPM),
            'company_ref': int(company_ref['id_company'])
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 201:
                QMessageBox.information(self, 'Success', 'Motor creado exitosamente')
                self.close()
            else:
                QMessageBox.warning(self, 'Error', f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"An error occurred: {str(e)}")
