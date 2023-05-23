from gui.MainWindow import MainWindow
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


def main():
    bart = QApplication([])
    mw = MainWindow()
    bart.exec_()


if __name__ == "__main__":
    main()
