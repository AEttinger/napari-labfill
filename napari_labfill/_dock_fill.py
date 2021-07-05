from magicgui import magic_factory
from magicgui import widgets
from skimage import segmentation
from skimage import filters
from typing_extensions import Annotated
from napari.layers.utils.stack_utils import split_channels
import numpy as np
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
        self.setObjectName('Flood fill')

        layout = QGridLayout()
        self.setLayout(layout)
        self.status = QLabel('Status', self)
        self.sig_val = QLabel('3', self)
        self.tol_val = QLabel('20', self)
        self.con_val = QLabel('32', self)

        self.sig_label = QLabel('Sigma', self)
        self.tol_label = QLabel('Tolerance', self)
        self.con_label = QLabel('Connectivity', self)

        self.abort_btn = QPushButton("Abort", self)
        self.reset_btn = QPushButton("Reset", self)

        self.progress_bar = QProgressBar()

        self.sig_slide = QSlider(Qt.Horizontal, self)
        self.sig_slide.setRange(0, 20)
        self.sig_slide.setValue(3)
        self.sig_slide.setSingleStep(1)
        self.sig_slide.valueChanged.connect(self.update_sig)

        self.tol_slide = QSlider(Qt.Horizontal, self)
        self.tol_slide.setRange(0, 99)
        self.tol_slide.setValue(20)
        self.tol_slide.setSingleStep(1)
        self.tol_slide.valueChanged.connect(self.update_tol)

        self.con_slide = QSlider(Qt.Horizontal, self)
        self.con_slide.setRange(0, 99)
        self.con_slide.setValue(32)
        self.con_slide.setSingleStep(1)
        self.con_slide.valueChanged.connect(self.update_con)

        self.ffill_btn = QPushButton(self)
        self.ffill_btn.setText("Toggle flood fill")
        self.ffill_btn.setCheckable(True)
        self.ffill_btn.setDown(False)
        self.ffill_btn.clicked.connect(self.button_switch)

        self.image = ''

        layout.addWidget(self.sig_label, 0, 0)
        layout.addWidget(self.sig_slide, 0, 1)
        layout.addWidget(self.sig_val, 0, 2)

        layout.addWidget(self.tol_label, 1, 0)
        layout.addWidget(self.tol_slide, 1, 1)
        layout.addWidget(self.tol_val, 1, 2)

        layout.addWidget(self.con_label, 2, 0)
        layout.addWidget(self.con_slide, 2, 1)
        layout.addWidget(self.con_val, 2, 2)

        layout.addWidget(self.ffill_btn, 3, 0, 3, 4)
        layout.addWidget(self.reset_btn, 4, 0, 4, 4)
        layout.addWidget(self.abort_btn, 5, 0, 5, 4)
        layout.addWidget(self.status, 6, 0, 6, 4)
        layout.addWidget(self.progress_bar, 7, 0, 7, 4)

    def update_sig(self, value):
        self.sig_val.setText(str(value))

    def update_tol(self, value):
        self.tol_val.setText(str(value))

    def update_con(self, value):
        self.con_val.setText(str(value))

    def button_switch(self):
        if self.ffill_btn.isChecked():
            self.status.setText('Flood fill on.')
            self.ffill_btn.setDown(True)
            # print(self.ffill_btn.isChecked())
        else:
            self.status.setText('Flood fill off.')
            self.ffill_btn.setDown(False)
            # print(self.ffill_btn.isChecked())


def update_layer(new_layer, layer_name):
    try:
        # if the layer exists, update the data
        viewer.layers[layer_name].data = new_layer
    except KeyError:
        raise


# long running function
@thread_worker
def _flood_fill(image, sigma, seed_point, connectivity, tolerance):
    # implement as thread worker as it may take time
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
    yield label_layer, kwargs


@thread_worker
def yield_gaussian(image, sigma):
    yield filters.gaussian(image, sigma=sigma)


def create_flood_fill_widget():
    # create controller widget
    w = FloodFillController()

    # function to initialize points and labels layers with same dims as image
    def init_layers():
        # check image dimensions
        if type(viewer.layers.selection.active) == napari.layers.image.image.Image:
            image = viewer.layers.selection.active
            if image.data.ndim > 3:
                w.status.setText('Please select a single channel image.')
            if image.data.ndim <= 3:
                empty = np.zeros(image.data.shape, dtype=np.dtype('uint16'))
                if 'Flood fill points' not in viewer.layers:
                    viewer.add_points(np.array([]), name='Flood fill points')
                if 'Flood fill labels' not in viewer.layers:
                    viewer.add_labels(empty, name='Flood fill labels')
                if 'Gaussian blur' not in viewer.layers:
                    viewer.add_image(filters.gaussian(image.data, sigma=w.sig_slide.value), name='Gaussian blur')
        else:
            w.status.setText('Please select an image layer.')

    # the following seems to work for checking the type of data
    def check_layers():
        for layer in viewer.layers:
            print(type(layer) == napari.layers.image.image.Image)
        # @viewer.layers.layer.mouse_drag_callbacks.append
        # def callback(layer, event):
        #    print(event.pos)
        #    print(layer.coordinates)

    w.ffill_btn.clicked.connect(init_layers)

    def on_yielded(image):
        gaussian_worker.pause()
        update_layer(image, 'Gaussian blur')

    w.sig_slide.valueChanged.connect(update_layer, 'Gaussian blur')

    # worker = _flood_fill(image, sigma)
    # w.ffill_btn.clicked.connect()

    # check if image exists

    # check if points layer exists

    # check if shapes layer exists


    return w


if __name__ == "__main__":
    viewer = napari.Viewer()
    w = create_flood_fill_widget()
    viewer.window.add_dock_widget(w)
    # sigma = w.sig_slide.value()
    # tolerance = w.tol_slide.value()
    # connectivity = w.con_slide.value()


    napari.run()
