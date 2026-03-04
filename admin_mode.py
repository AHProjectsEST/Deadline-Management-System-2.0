from PySide6.QtCore import QDate, Signal
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateTimeEdit,
    QDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class admin_mode(QDialog):
    def __init__(self, partent=None):
        super().__init__(partent)
        self.setWindowTitle(f"Login")
        layout = QVBoxLayout(self)

        self.adm_label = QLabel("Enter admin password:")
        layout.addWidget(self.adm_label)

        self.password_inp = QLineEdit()
        self.password_inp.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_inp)

        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self.accept)
        layout.addWidget(self.ok_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        self.cancel_btn.setObjectName("cancel_button")

        layout.addWidget(self.cancel_btn)

    def get_password_inp(self):
        return self.password_inp.text()
