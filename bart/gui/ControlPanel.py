from utils.ImageEffects import ImageEffects as effects
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel, QWidget
from gui.Slider import Slider
from utils.State import State


class ControlPanel(QWidget):
    """Custom QWidget containing control sliders and buttons"""

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout()
        self.widgets = {
            "rotate_btn": QPushButton(text="Otočit o 90°", parent=self),
            "invert_btn": QPushButton(text="Inverze barev", parent=self),
            "vignette_btn": QPushButton(text="Vinětace", parent=self),
            "emboss_btn": QPushButton(text="Emboss", parent=self),
            "sharpen_label": QLabel(text="Zaostření", parent=self),
            "sharpen_sldr": Slider(Qt.Horizontal, parent, 0, 2),
            "blur_label": QLabel(text="Rozmazání", parent=self),
            "blur_sldr": Slider(Qt.Horizontal, parent, 1, 15, is_odd=True),
            "brightness_label": QLabel(text="Jas", parent=self),
            "brightness_sldr": Slider(Qt.Horizontal, parent, 0, 20),
            "contrast_label": QLabel(text="Kontrast", parent=self),
            "contrast_sldr": Slider(Qt.Horizontal, parent, 0, 2),
            "perlin_label": QLabel(text="Šum", parent=self),
            "perlin_noise_sldr": Slider(Qt.Horizontal, parent, 0, 2),
            "denoise_label": QLabel(text="Redukce šumu", parent=self),
            "denoise_sldr": Slider(Qt.Horizontal, parent, 0, 50),
            "reset_btn": QPushButton(text="Reset", parent=self),
        }

        self.widgets["rotate_btn"].clicked.connect(self.on_rotate_btn_click)
        self.widgets["invert_btn"].clicked.connect(self.on_invert_btn_click)
        self.widgets["vignette_btn"].clicked.connect(self.on_vignette_btn_click)
        self.widgets["emboss_btn"].clicked.connect(self.on_emboss_btn_click)
        self.widgets["reset_btn"].clicked.connect(self.on_reset_btn_click)

        self.widgets["sharpen_sldr"].valueChanged.connect(self.on_sharpen_sldr_move)
        self.widgets["blur_sldr"].valueChanged.connect(self.on_blur_sldr_move)
        self.widgets["brightness_sldr"].valueChanged.connect(
            self.on_brightness_sldr_move
        )
        self.widgets["contrast_sldr"].valueChanged.connect(self.on_contrast_sldr_move)
        self.widgets["perlin_noise_sldr"].valueChanged.connect(self.on_noise_sldr_move)
        self.widgets["denoise_sldr"].valueChanged.connect(self.on_denoise_sldr_move)

        self.init_layout()

    def init_layout(self):
        """Initialize widget layout"""
        for w in self.widgets.values():
            self.layout.addWidget(w)
        self.setLayout(self.layout)

    def _return_to_previous_state(self) -> State:
        """Fallback to previous state"""
        return self.parent.states.pop()

    def on_rotate_btn_click(self):
        """Rotate image by 90 degrees"""
        # TODO: use base image only
        new_state = self.parent.states[-1]
        new_state.rotation = new_state.rotation + 90
        new_state.image = effects.get_rotated_image(self.parent.states[0].image, 90)
        self.parent.states.append(new_state)
        self.parent.show()

    def on_invert_btn_click(self):
        """Invert image colors"""
        self.parent.destroy()
        if self.parent.states[-1].is_inverted:
            return
        new_state = self.parent.states[-1]
        previous_image = self.parent.states[0].image
        new_state.image = effects.get_inverted_image_colors(previous_image)
        new_state.is_inverted = True
        self.parent.states.append(new_state)
        self.parent.show()

    def on_warp_btn_click(self):
        """Correct image using point selection"""
        self.parent.destroy()
        # TODO: gui dialog for point selection, calls effect
        pass

    def on_vignette_btn_click(self):
        """Add vignette filter"""
        self.parent.destroy()
        if self.parent.states[-1].is_vignetted:
            return
        new_state = self.parent.states[-1]
        new_state.image = effects.get_vignette_image(self.parent.states[0].image)
        new_state.is_vignetted = True
        self.parent.states.append(new_state)
        self.parent.show()

    def on_emboss_btn_click(self):
        """Emboss image"""
        self.parent.destroy()
        if self.parent.states[-1].is_embossed:
            return
        new_state = self.parent.states[-1]
        new_state.image = effects.get_embossed_image(self.parent.states[0].image)
        new_state.is_embossed = True
        self.parent.states.append(new_state)
        self.parent.show()

    def on_sharpen_sldr_move(self, value):
        """Sharpen"""
        self.parent.destroy()
        new_state = self.parent.states[-1]
        previous_image = self.parent.states[0].image
        new_state.image = effects.get_sharpen_image(previous_image, value)
        self.parent.states.append(new_state)
        self.parent.show()

    def on_blur_sldr_move(self, value):
        """Set blur"""
        # only of odd numbers
        self.parent.destroy()
        if value % 2 == 1:
            new_state = self.parent.states[-1]
            previous_image = self.parent.states[0].image
            new_state.image = effects.get_blured_image(previous_image, value)
            self.parent.states.append(new_state)
            self.parent.show()
        else:
            pass

    def on_brightness_sldr_move(self, value):
        """Set brightness"""
        self.parent.destroy()
        new_state = self.parent.states[-1]
        previous_image = self.parent.states[0].image
        new_state.image = effects.get_brightness_modified_image(previous_image, value)
        self.parent.states.append(new_state)
        self.parent.show()

    def on_contrast_sldr_move(self, value):
        """Set contrast"""
        self.parent.destroy()
        new_state = self.parent.states[-1]
        previous_image = self.parent.states[0].image
        new_state.image = effects.get_contrast_modified_image(previous_image, value)
        self.parent.states.append(new_state)
        self.parent.show()

    def on_noise_sldr_move(self, value):
        """Add noise"""
        self.parent.destroy()
        new_state = self.parent.states[-1]
        previous_image = self.parent.states[0].image
        new_state.image = effects.get_noise(previous_image, value / 100)
        self.parent.states.append(new_state)
        self.parent.show()

    def on_denoise_sldr_move(self, value):
        """Denoise"""
        self.parent.destroy()
        new_state = self.parent.states[-1]
        previous_image = self.parent.states[0].image
        new_state.image = effects.get_denoised_image(previous_image, value)
        self.parent.states.append(new_state)
        self.parent.show()

    def on_reset_btn_click(self):
        """Resets all settings"""
        self.parent.destroy()
        self.parent.clear()
        self.parent.show()
