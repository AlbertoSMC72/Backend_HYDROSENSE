from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from session import Session
from add_motor_window import AddMotorWindow

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')
        self.setGeometry(200, 200, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Welcome to HYDROSENSE!')
        layout.addWidget(self.label)

        self.button_add_motors = QPushButton('Agregar Motores')
        self.button_add_motors.clicked.connect(self.open_add_motor_window)
        layout.addWidget(self.button_add_motors)

        self.button_view_graphs = QPushButton('Ver Gráficas')
        self.button_view_graphs.clicked.connect(self.view_graphs)
        layout.addWidget(self.button_view_graphs)

        self.button_view_reports = QPushButton('Ver Reportes')
        self.button_view_reports.clicked.connect(self.view_reports)
        layout.addWidget(self.button_view_reports)

        self.setLayout(layout)

    def open_add_motor_window(self):
        self.add_motor_window = AddMotorWindow()
        self.add_motor_window.show()

    def view_graphs(self):
        session = Session()
        user_data = session.get_user_data()
        print('Ver Gráficas button clicked')
        print('User Data:', user_data)

    def view_reports(self):
        session = Session()
        user_data = session.get_user_data()
        print('Ver Reportes button clicked')
        print('User Data:', user_data)
