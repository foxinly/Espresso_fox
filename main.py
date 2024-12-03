import sys
import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.initUI()

    def initUI(self):
        self.create_btn.clicked.connect(self.create_coffee)
        self.change_btn.clicked.connect(self.change_coffee)
        self.close_btn.clicked.connect(self.close_coffee)

    def create_coffee(self):
        pass

    def change_coffee(self):
        pass

    def close_coffee(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffee()
    ex.show()
    sys.exit(app.exec())
