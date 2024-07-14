from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from session import Session

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')
        self.setGeometry(200, 200, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Welcome to the main window!')
        layout.addWidget(self.label)

        self.button_add_motors = QPushButton('Agregar Motores')
        self.button_add_motors.clicked.connect(self.add_motors)
        layout.addWidget(self.button_add_motors)

        self.button_view_graphs = QPushButton('Ver Gráficas')
        self.button_view_graphs.clicked.connect(self.view_graphs)
        layout.addWidget(self.button_view_graphs)

        self.button_view_reports = QPushButton('Ver Reportes')
        self.button_view_reports.clicked.connect(self.view_reports)
        layout.addWidget(self.button_view_reports)

        self.setLayout(layout)

    def add_motors(self):
        session = Session()
        user_data = session.get_user_data()
        print('Agregar Motores button clicked')
        print('User Data:', user_data)

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
