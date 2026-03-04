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


class admin_window(QWidget):
    closed = Signal()

    def __init__(self, con):
        super().__init__()
        self.setWindowTitle("Admin Panel")
        x_size = 800
        y_size = 600
        self.resize(x_size, y_size)

        try:
            self.con = con

            layout = QVBoxLayout(self)

            self.table = QTableWidget()
            self.table.setColumnCount(3)
            self.table.setHorizontalHeaderLabels(["Name", "Deadline", "Done"])
            # self.table.horizontalHeader().setStretchLastSection(True)
            header = self.table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.ResizeToContents)

            layout.addWidget(self.table)

            self.update_btn = QPushButton("Update Selected")
            self.delete_btn = QPushButton("Delete Selected")
            self.exit_adm_btn = QPushButton("Exit admin mode")

            self.exit_adm_btn.clicked.connect(self.exit_adm_window)
            self.update_btn.clicked.connect(self.update_deadline)
            self.delete_btn.clicked.connect(self.delete_deadline)

            layout.addWidget(self.update_btn)
            layout.addWidget(self.delete_btn)
            layout.addWidget(self.exit_adm_btn)

            self.load_deadlines()
        except Exception as exce:
            print("ADMIN WINDOW ERROR:", exce)
            raise

        self.setStyleSheet(QApplication.instance().styleSheet())

    def load_deadlines(self):
        rows = self.con.execute("SELECT * FROM deadlines ORDER BY date").fetchall()

        self.table.setRowCount(len(rows))

        for row_index, (name, date, done) in enumerate(rows):
            self.table.setItem(row_index, 0, QTableWidgetItem(name))
            self.table.setItem(row_index, 1, QTableWidgetItem(str(date)))
            self.table.setItem(row_index, 2, QTableWidgetItem(str(done)))

    def update_deadline(self):
        row = self.table.currentRow()
        if row < 0:
            return
        name = self.table.item(row, 0).text()
        date = self.table.item(row, 1).text()
        done = self.table.item(row, 2).text()

        self.con.execute(
            "UPDATE deadlines set date = ?, done_status = ? WHERE name = ?",
            [date, done, name],
        )

    def delete_deadline(self):
        row = self.table.currentRow()
        if row < 0:
            return

        name = self.table.item(row, 0).text()

        self.con.execute("DELETE FROM deadlines WHERE name = ?", [name])
        print(f"Deleted deadline {name}")
        self.table.removeRow(row)
        self.refresh()

    def refresh(self):
        self.table.clearContents()
        self.load_deadlines()

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

    def exit_adm_window(self):

        self.close()
