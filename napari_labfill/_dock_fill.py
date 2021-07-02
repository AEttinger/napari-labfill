from magicgui import magic_factory
from magicgui import widgets
from skimage import segmentation
from skimage import filters
from typing_extensions import Annotated

import napari
from napari.types import ImageData

from qtpy.QtWidgets import (
    QGridLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QWidget,
    QSlider,
)

from qtpy.QtCore import Qt

from napari.qt.threading import thread_worker


class FloodFillController(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout()
        self.setLayout(layout)
        self.status = QLabel('Status', self)
        self.sig_label = QLabel('Sigma', self)
        self.tol_label = QLabel('Tolerance', self)
        self.con_label = QLabel('Connectivity', self)
        self.abort_btn = QPushButton("Abort", self)
        self.reset_btn = QPushButton("Reset", self)
        self.progress_bar = QProgressBar()
        self.sig_slide = QSlider(Qt.Horizontal, self)
        self.tol_slide = QSlider(Qt.Horizontal, self)
        self.con_slide = QSlider(Qt.Horizontal, self)
        self.ffill_btn = QPushButton(self)
        self.ffill_btn.setText("Toggle flood fill")
        self.ffill_btn.setCheckable(True)
        self.ffill_btn.setDown(True)

        layout.addWidget(self.sig_label, 0, 0)
        layout.addWidget(self.sig_slide, 0, 1)
        layout.addWidget(self.tol_label, 1, 0)
        layout.addWidget(self.tol_slide, 1, 1)
        layout.addWidget(self.con_label, 2, 0)
        layout.addWidget(self.con_slide, 2, 1)
        layout.addWidget(self.ffill_btn, 3, 0, 3, 3)
        layout.addWidget(self.reset_btn, 4, 0, 4, 3)
        layout.addWidget(self.abort_btn, 5, 0, 5, 3)
        layout.addWidget(self.status, 6, 0, 6, 3)
        layout.addWidget(self.progress_bar, 7, 0, 7, 3)


def update_layer(new_layer):
    try:
        # if the layer exists, update the data
        viewer.layers['flood fill labels'].data = new_layer
    except KeyError:
        # otherwise add it to the viewer
        viewer.add_layer(
            new_layer, name='flood fill labels'
        )


# long running function
@thread_worker(connect={"yielded": update_layer})
def _flood_fill(image, sigma, seed_point, connectivity, tolerance):
    # implement as thread worker as it may take soje time
    gaussian = filters.gaussian(
        image,
        sigma=sigma
    )
    flood = segmentation.flood(
        gaussian,
        seed_point=seed_point,
        connectivity=connectivity,
        tolerance=tolerance
    )
    label_layer = flood
    kwargs = dict(
        edge_color="red",
        edge_width=2,
        face_color="transparent",
    )
    yield (label_layer, kwargs)


def create_flood_fill_widget():
    w = FloodFillController()
    # worker = _flood_fill(image, sigma)
    w.
    return w


if __name__ == "__main__":
    viewer = napari.Viewer()
    w = create_flood_fill_widget()
    viewer.window.add_dock_widget(w)
    # sigma = w.sig_slide.value()
    # tolerance = w.tol_slide.value()
    # connectivity = w.con_slide.value()

    napari.run()
