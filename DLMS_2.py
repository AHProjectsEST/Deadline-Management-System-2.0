import os
from datetime import datetime

import duckdb
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

version_control = "2.01"  # first layout creation
version_control = "2.31"  # connected Duckdb, and deadline list
version_control = "2.47"  # main functionality done, themes and admin panel started


class mainwin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Deadline management system {version_control}")
        x_size = 1600
        y_size = 800
        self.resize(x_size, y_size)
        # --- Central widget required for QMainWindow ---
        central = QWidget()
        self.setCentralWidget(central)

        self.path_to_DB_file = os.getcwd() + r"/DLMS2_db.duckdb"
        try:
            if not self.path_to_DB_file.endswith(".duckdb"):
                self.path_to_DB_file += ".duckdb"
            self.con = duckdb.connect(self.path_to_DB_file)
            print(self.con)
        except:
            QMessageBox.warning(
                self,
                "Error",
                "Incorrect database path or database allready open in other applications",
            )
            print(self.path_to_DB_file, "is flawed!")

        # ============================================================
        # --- Main horisontal area
        # ============================================================
        main_layout = QHBoxLayout()
        central.setLayout(main_layout)

        # ============================================================
        # --- adding left panel
        # ============================================================
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)

        # ============================================================
        # Create widgets
        # ============================================================
        self.add_label = QLabel("Add upcoming task name:")
        self.DL_label_entry = QLineEdit("Insert name!")
        self.date_label = QLabel("Add the due date")
        self.DL_date = QDateTimeEdit(QDate.currentDate())
        self.DL_date.setDisplayFormat("yyyy-MM-dd hh:mm")
        self.add_DL_btn = QPushButton("Add deadline")

        widgets_left = [
            self.add_label,
            self.DL_label_entry,
            self.date_label,
            self.DL_date,
            self.add_DL_btn,
        ]

        for w in widgets_left:
            w.setSizePolicy(
                QSizePolicy.Expanding,
                QSizePolicy.Preferred,  # vertical behavior
            )

        for w in widgets_left:
            left_layout.addWidget(w)

        # fix left panel width
        # left_panel.setFixedWidth(x_size / 5)
        # Add left panel to main layout
        main_layout.addWidget(left_panel)

        # ==================================
        #  RIGHT LAYOUT
        # ==================================

        right_side = QWidget()
        right_layout = QVBoxLayout()
        right_side.setLayout(right_layout)

        # ---------------------------------------------
        # add all the right side widgets here
        # -------------------------------------------
        testing_w = QLabel("List of upcoming deadlines")
        right_layout.addWidget(testing_w)

        # List widget
        #
        self.list_widget = QListWidget()
        right_layout.addWidget(self.list_widget)

        self.load_deadlines()

        main_layout.addWidget(right_side)

        main_layout.setStretch(0, 1)  # left panel gets 1 part
        main_layout.setStretch(1, 4)  # right panel gets 4 parts

        # =================================================================================================================================
        # --- MAIN AREA ---
        # =================================================================================================================================
        main_area = QWidget()
        main_area_layout = QVBoxLayout()
        main_area.setLayout(main_area_layout)

        right_layout.addWidget(main_area)

        # =================================================================================================================================
        # --- BOTTOM PANEL ---
        # This is vertical layout. Later will be added horisontal layout on top of it to modify plot
        # =================================================================================================================================
        bottom_panel = QWidget()
        # initial vertical layer
        bottom_layout = QVBoxLayout()
        bottom_panel.setLayout(bottom_layout)
        # stuff for bottom panel
        self.bottom_lay_text = QLabel("Bottom panel content")
        # bottom_layout.addWidget(self.bottom_lay_text)

        self.theme_select = QComboBox()
        self.theme_select.currentTextChanged.connect(self.apply_theme)
        self.theme_select.blockSignals(True)
        self.theme_select.addItems(self.list_themes())
        self.theme_select.blockSignals(False)

        self.exit_btn = QPushButton("Quit")
        self.exit_btn.setObjectName("Quit_button")
        self.exit_btn.clicked.connect(self.exit_DLMS2)

        # horisontal layer for buttons
        control_panel = QHBoxLayout()

        # stuff for control panel
        self.adm_button = QPushButton("Admin mode")
        control_panel.addWidget(self.theme_select)
        control_panel.addWidget(self.adm_button)
        control_panel.addWidget(self.exit_btn)
        """for rw in bottom_widgets:
            control_panel.addWidget(rw)"""

        # adding vertical layer features
        bottom_layout.addLayout(control_panel)

        # setting bottom panel height
        bottom_panel.setFixedHeight(80)
        right_layout.addWidget(bottom_panel)

        self.add_DL_btn.clicked.connect(self.add_deadline)
        self.adm_button.clicked.connect(self.open_adm_mode)

        # loading last used theme
        self.load_last_theme()

    def update_status(self, name, state):
        done = bool(state)
        self.con.execute(
            "UPDATE deadlines SET done_status = ? WHERE name = ?", [done, name]
        )

    def load_deadlines(self):
        self.list_widget.clear()
        try:
            self.deadlines_ddb = self.con.execute(
                "SELECT * FROM deadlines ORDER BY date"
            ).fetchall()
        except:
            QMessageBox.warning(self, "Error", "Database error, see terminal log")
            print(self.path_to_DB_file, "is flawed!")

        date_now = datetime.now()
        for name, date, done_stat in self.deadlines_ddb:
            # print(name, date, done_stat)
            if name == None:
                continue
            checkbox = QCheckBox(f"   {name}    -    {date}")
            checkbox.setChecked(bool(done_stat))

            diff_date = date - date_now
            days = diff_date.days

            """if days >= 0 and days <= 1:
                checkbox.setObjectName("task_past_deadline")

            if 0 <= days <= 1 and ("exa" in name.lower() or "eksa" in name.lower()):
                checkbox.setStyleSheet("color: red;")

                checkbox.setStyleSheet("color: red;")
            elif "exa" in name.lower() or "eksa" in name.lower() and days > 1:
                checkbox.setStyleSheet("color: #FF8787;")

            if days < 0 and done_stat == False:
                checkbox.setStyleSheet("color: #9EC8FF;")
            elif days < 0:
                checkbox.setStyleSheet("color: #ADF0FF;")"""

            item = QListWidgetItem(self.list_widget)
            # item.setSizeHint(QSize(item.sizeHint().width(), 40))
            self.list_widget.setItemWidget(item, checkbox)
            self.list_widget.setSpacing(8)
            checkbox.stateChanged.connect(
                lambda state, name=name: self.update_status(name, state)
            )

    def add_deadline(self):
        dl_name_new = self.DL_label_entry.text()
        if dl_name_new == "Insert name!":
            QMessageBox.warning(
                self, "Invalid name", "Enter valid Deadline name please!"
            )
            return None
        dl_date_time_new = self.DL_date.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        done_stat_new = False

        date_now = datetime.now()
        deadline_datetime = datetime.strptime(dl_date_time_new, "%Y-%m-%d %H:%M:%S")
        if deadline_datetime < date_now:
            QMessageBox.warning(self, "Invalid date", "Date can not be in the past!")
            return None

        self.update_DL_DB = self.con.execute(
            "INSERT INTO deadlines (name, date, done_status) VALUES (?, ?, ?)",
            [dl_name_new, dl_date_time_new, done_stat_new],
        )

        print(f"added deadline {dl_name_new} {dl_date_time_new}")
        self.load_deadlines()

    def open_adm_mode(self):
        dialog = admin_mode(self)

        if dialog.exec():  # returns true if ok was pressed
            password = dialog.get_password_inp()
            self.passw_db = self.con.execute(
                "SELECT * FROM admin_pass ORDER BY date"
            ).fetchall()

            for passw, date in self.passw_db:
                if password == passw:
                    self.adm_win = admin_window(self.con)
                    self.adm_win.closed.connect(self.load_deadlines)
                    self.adm_win.show()
                    return

            QMessageBox.warning(self, "Access denied", "Incorrect password")

    def list_themes(self):
        self.work_dir = os.getcwd()
        self.theme_folder = self.work_dir + "/themes"

        if not os.path.exists(self.theme_folder):
            os.makedirs(self.theme_folder)

        self.theme_names = []

        for file in os.listdir(self.theme_folder):
            if file.endswith(".qss"):
                file_strip = file.strip(".qss")
                self.theme_names.append(file_strip)
        return self.theme_names

    def apply_theme(self, theme_name):
        theme_path = f"{self.theme_folder}/{theme_name}.qss"

        with open(theme_path, "r") as theme:
            style = theme.read()
            QApplication.instance().setStyleSheet(style)

        self.con.execute("UPDATE last_theme SET theme_select = ?;", [theme_name])

    def load_last_theme(self):
        self.last_theme_db = self.con.execute(
            "SELECT theme_select FROM last_theme"
        ).fetchone()

        if self.last_theme_db:
            theme_name = self.last_theme_db[0]
            self.apply_theme(theme_name)

            index = self.theme_select.findText(theme_name)
            if index >= 0:
                self.theme_select.blockSignals(True)
                self.theme_select.setCurrentIndex(index)
                self.theme_select.blockSignals(False)

    def exit_DLMS2(self):
        exit()


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


app = QApplication()


window = mainwin()
window.show()
app.exec()
