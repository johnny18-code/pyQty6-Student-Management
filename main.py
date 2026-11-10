
import concurrent
from multiprocessing import connection
from PyQt6.QtWidgets import QApplication, QBoxLayout, QDial, QPushButton, QStatusBar, QTableWidget, QTableWidgetItem, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, QComboBox, QMainWindow, QDialog, QToolBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon  # QIcon for QAction for Image Icon
from PyQt6.QtCore import Qt
import sys
import sqlite3

# Edit Menu and Sub Search item  - 11/9/2026 - Done 11/9/2026
# Added actual Edit Functionality - 11/9/2026 - Done on 11/9/2026
# Delete the record - 11/9/2026 - Done 11/11/2026
# About - 11/9/2026 - Done on 11/11/2026


class MainWindow(QMainWindow):  # QMainWindow for Larger Apps and with Different Windows needed
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 500)

        # Menu Bars
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Sub Window / Sub Item
        # with "self" connects to the MainWindow Class
        # Qaction creates sub-window? which you can then append to menuBar?
        add_student_action = QAction(
            QIcon("icons\\add.png"), "Add Student", self)
        # using addAction Method?
        add_student_action.triggered.connect(
            self.insert_student)  # triggers to a method
        file_menu_item.addAction(add_student_action)

        edit_student_action = QAction(
            QIcon("icons\\search.png"), "Search", self)
        edit_student_action.triggered.connect(self.edit_sub)
        edit_menu_item.addAction(edit_student_action)

        # with "self" connects to the MainWindow Class
        add_about_window = QAction("About", self)
        help_menu_item.addAction(add_about_window)
        add_about_window.triggered.connect(self.aboutSub)
        # something wiht the help on MAC? if HELP doesn't show
        # use this; add_about_window.setMenuRole(QAction.MenuRole.NoRole)

        # -------------------------------------------------------------------#

        # plot table as the instance of the Main Window
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ("ID", "NAME", "COURSE", "PHONE-NUMBER"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # --------------------------------------------------------------------#
        # Creating tool bars
        # Most use case is for shortcuts

        # Add student
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        # Search
        toolbar.addAction(edit_student_action)

        # --------------------------------------------------------------------#
        # Create Status Bars
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell Click
        self.table.cellClicked.connect(self.showStatusBar)

    def showStatusBar(self, s):
        print(s)

        # edit tool bar
        editButton = QPushButton("Edit Student")
        editButton.clicked.connect(self.showEditDialog)

        # delete tool bar
        deleteButton = QPushButton("Delete Student")
        deleteButton.clicked.connect(self.deleteDialog)

        pusButtonChildren = self.findChildren(QPushButton)
        if pusButtonChildren:
            for child in pusButtonChildren:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(editButton)
        self.statusbar.addWidget(deleteButton)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)  # each call to load it will reset to 0

        for row_x, row_data in enumerate(result):
            print(row_x, row_data)
            self.table.insertRow(row_x)  # initialized index row
            # loop as many columns in the row then insert to that row per each column
            for column, data in enumerate(row_data):
                print(row_x, column, data)
                self.table.setItem(row_x, column, QTableWidgetItem(str(data)))
        connection.close()

    def insert_student(self):
        print("Call Dialog -- Inserting New Student")

        dialog = InsertDialog()

        dialog.exec()

    def edit_sub(self):
        print("Dialog Edit")
        dialog = EditDialog()
        dialog.exec()

    def showEditDialog(self):
        print("Cell Clicked Edit Dialog")
        dialog = ActualEditDialog()
        dialog.exec()

    def deleteDialog(self):
        print("Delete Dialog")
        dialog = ActualDeleteDialog()
        dialog.exec()

    def aboutSub(self):
        dialog = ActualAboutDialog()
        dialog.exec()


class ActualAboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Success")
        self.setText("This is Johnny -- Practicing Python CLASS OOP")


class ActualEditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Student Dialog")
        index = window.table.currentRow()  # return current selected row

        print(index, "Index")
        # returns that actual row and actual cell
        self.id = window.table.item(index, 0).text()
        self.old_name = window.table.item(index, 1).text()
        self.old_course = window.table.item(index, 2).text()
        self.old_phone_nume = window.table.item(index, 3).text()

        layout = QVBoxLayout()
        self.current_student_name = QLineEdit(self.old_name)
        layout.addWidget(self.current_student_name)

        self.current_course_name = QComboBox()
        courses = ["Math", "Science", "Data Science",
                   "Computer Science", "AI Prompter ", "Astronomy", "Physics", "IT", "Biology"]
        self.current_course_name.addItems(courses)
        self.current_course_name.setCurrentText(self.old_course)
        layout.addWidget(self.current_course_name)

        self.current_phone_number = QLineEdit(self.old_phone_nume)
        layout.addWidget(self.current_phone_number)

        update_button = QPushButton("Update Record")
        layout.addWidget(update_button)
        update_button.clicked.connect(self.updateNow)
        self.setLayout(layout)

    def updateNow(self):
        print("updating...")
        # update based on ID
        int_id = int(self.id)
        # self.current_course_name.itemText(self.current_course_name.currentIndext())
        update_course = self.current_course_name.currentText()
        update_name = self.current_student_name.text()
        update_number = int(self.current_phone_number.text())

        connection = sqlite3.connect("database.db")
        connection.execute("UPDATE students SET name = ?, course = ?, mobile = ? where ID = ? ", (
            update_name, update_course, update_number, int_id))
        connection.commit()
        connection.close()
        window.load_data()


class ActualDeleteDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()
        # print Delete Dialog
        # pop-up? if yes, delete from table if no rollback? or nothing close window
        self.setWindowTitle("Delete Dialog")

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete?")

        yes = QPushButton("Yes")
        yes.clicked.connect(self.commitDelete)

        no = QPushButton("No")
        no.clicked.connect(self.doNotDelete)

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 2, 0)
        self.setLayout(layout)  # show

    def commitDelete(self):

        index = window.table.currentRow()  # return current selected row
        id = window.table.item(index, 0).text()
        name = window.table.item(index, 1).text()

        #
        connection = sqlite3.connect("database.db")
        result = connection.execute(
            "DELETE FROM students WHERE ID = ? and NAME = ?", (id, name))
        connection.commit()
        connection.close()

        # close the current dialoag

        # QMessageBox like a Mini Dialog
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was deleted successfully")
        confirmation_widget.exec()

        self.close()
        window.load_data()

        # then close the dialog

    def doNotDelete(self):
        self.close()  # just close


class InsertDialog(QDialog):  # create instance Dialog?

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("New Student Dialog --")

        self.setFixedHeight(300)
        self.setFixedWidth(300)

        layout = QVBoxLayout()  # Stacked down
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Student Name")
        layout.addWidget(self.student_name)

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("self.mobile")
        layout.addWidget(self.mobile)

        self.course_name = QComboBox()
        courses = ["Biology", "IT", "Astronomy"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        button = QPushButton("Insert New Student")
        layout.addWidget(button)
        button.clicked.connect(self.add_student)
        self.setLayout(layout)

    def add_student(self):
        print("adding student")
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?,?,?)", (
            self.student_name.text(), self.course_name.currentText(), self.mobile.text()))
        connection.commit()
        cursor.close()

        # refresh?
        window.load_data()  # this window instance can be called anywhere but only inside of method?


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Student Dialog --")

        self.setFixedHeight(300)
        self.setFixedWidth(300)

        # Stacked down # live a dive class, inside of it you can append widigets
        layout = QVBoxLayout()
        self.input_name_search = QLineEdit()
        layout.addWidget(self.input_name_search)

        button = QPushButton("Search Student")
        layout.addWidget(button)
        button.clicked.connect(self.search_student)

        self.setLayout(layout)  # Show the Layout~?

    def search_student(self):
        print("Self Student")
        # This will highligh the row in the table...
        name = self.input_name_search.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = connection.execute(
            "SELECT * FROM students where name = ? ", (name,))
        result = list(result)  # list of tuples
        items = window.table.findItems(
            name, Qt.MatchFlag.MatchFixedString)  # find the match
        for item in items:
            window.table.item(item.row(), 1).setSelected(
                True)  # this is where it actually hightlights
        cursor.close()
        connection.close()


if __name__ == "__main__":
    print("Student Management System")
    app = QApplication(sys.argv)  # sys.argv allows command line arguments?
    window = MainWindow()
    window.load_data()
    window.show()
    sys.exit(app.exec())
