from cv2 import cvtColor, COLOR_BGR2RGB
from imutils import resize
from gui.ControlPanel import ControlPanel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QMenuBar, QLabel, QGridLayout, QAction, QFileDialog
from utils.State import State
from utils.file_utils import open_image, save_image
from gui.Slider import Slider


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.main_menu = QMenuBar()
        self.image_container = QLabel()
        self.control_panel = ControlPanel(self)
        self.control_panel.setEnabled(False)
        self.layout = QGridLayout()
        self.image = None
        self.states = []
        self.setFixedWidth(1000)
        self.setFixedHeight(800)
        self.init_layout()

    def init_layout(self) -> None:
        """
        Initialize layout
        """
        self.setWindowTitle("b.ART")
        # setup file menu
        file_menu = self.main_menu.addMenu("Soubor")

        # open file
        open = QAction("Otevřít", self)
        open.setShortcut("Ctrl+O")
        open.triggered.connect(self.open_dialog)
        file_menu.addAction(open)

        # save file
        open = QAction("Uložit", self)
        open.setShortcut("Ctrl+S")
        open.triggered.connect(self.save_dialog)
        file_menu.addAction(open)

        # set layout
        self.layout.addWidget(self.main_menu, 0, 0)
        self.layout.addWidget(self.image_container, 1, 0)
        self.layout.addWidget(self.control_panel, 1, 1)
        self.layout.setColumnStretch(0, 6)
        self.layout.setRowStretch(1, 1)
        self.setLayout(self.layout)

        self.showMaximized()
        self.show()

    def open_dialog(self):
        """
        Show open file dialog
        """
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Otevřít obrázek",
            "",
            "PNG (*.png);;" "JPEG (*.jpeg);;",
        )
        if file_name:
            self.image = open_image(file_name)
            self.clear()
            self.show()
            self.control_panel.setEnabled(True)

    def save_dialog(self):
        """
        Show save file dialog
        """
        # TODO: keep only last state after save
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Uložit obrázek",
            "",
            "PNG (*.png);;" "JPEG (*.jpeg);;",
        )
        save_image(file_name, self.states[-1].image)
        self.clear()

    def show(self) -> None:
        """
        Update image container
        """
        if len(self.states):
            image = resize(self.states[-1].image, width=800)
            frame = cvtColor(image, COLOR_BGR2RGB)
            image = QImage(
                frame,
                frame.shape[1],
                frame.shape[0],
                frame.strides[0],
                QImage.Format_RGB888,
            )
            q = QPixmap.fromImage(image)
            q.scaled(64, 64, Qt.KeepAspectRatio)
            self.image_container.setPixmap(q)

    def clear(self):
        """
        Retrieve default state
        """
        self.states.clear()
        self.states.append(State(self.image))
        for w in self.control_panel.widgets.values():
            if isinstance(w, Slider):
                w.reset()

    def destroy(self):
        """
        Destroy previous filter
        """
        self.states.clear()
        self.states.append(State(self.image))
