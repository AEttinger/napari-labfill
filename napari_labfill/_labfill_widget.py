import napari
from napari_plugin_engine import napari_hook_implementation
from qtpy.QtWidgets import QWidget, QHBoxLayout, QPushButton

viewer = napari.Viewer()


# define only class for gui
class LabFillQWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.btn = QPushButton(self)
        # add parameter inputs
        # threshold
        # sigma
        # connected pixels
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.btn)


# connect to gui
def create_labfill_widget():
    lf = LabFillQWidget()


@viewer.layers.layer.mouse_drag_callbacks.append
def callback(layer, event):
    print(event.pos)
    print(layer.coordinates)


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    # you can return either a single widget, or a sequence of widgets
    return LabFillQWidget
