from napari_plugin_engine import napari_hook_implementation
from qtpy.QtWidgets import QWidget, QHBoxLayout, QPushButton
from magicgui import magic_factory


class LabFillQWidget(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer
        self.isActive = True

        self.btn = QPushButton(self)
        self.btn.setText("Flood fill")
        self.btn.setCheckable(True)
        self.btn.setDown(True)
        self.btn.toggled.connect(self._on_click)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.btn)

    def _on_click(self):
        if self.isActive:
            self.btn.setDown(False)
            self.isActive = not self.isActive
            print("Flood fill is {}.".format(self.isActive))
        else:
            self.btn.setDown(True)
            self.isActive = not self.isActive
            print("Flood fill is {}.".format(self.isActive))


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    # you can return either a single widget, or a sequence of widgets
    return LabFillQWidget
