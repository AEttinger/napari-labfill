import napari
import time

from napari.qt.threading import thread_worker
from qtpy.QtWidgets import QLineEdit, QLabel, QWidget, QVBoxLayout
from qtpy.QtGui import QDoubleValidator


@thread_worker
def multiplier():
    total = 1
    while True:
        time.sleep(0.1)
        new = yield total
        total *= new if new is not None else 1
        if total == 0:
            return "Game Over!"


viewer = napari.Viewer()

# make a widget to control the worker
# (not the main point of this example...)
widget = QWidget()
layout = QVBoxLayout()
widget.setLayout(layout)
result_label = QLabel()
line_edit = QLineEdit()
line_edit.setValidator(QDoubleValidator())
layout.addWidget(line_edit)
layout.addWidget(result_label)
viewer.window.add_dock_widget(widget)

# create the worker
worker = multiplier()


# define some callbacks
def on_yielded(value):
    worker.pause()
    result_label.setText(str(value))
    line_edit.setText('1')


def on_return(value):
    line_edit.setText('')
    line_edit.setEnabled(False)
    result_label.setText(value)


def send_next_value():
    worker.send(float(line_edit.text()))
    worker.resume()


worker.yielded.connect(on_yielded)
worker.returned.connect(on_return)
line_edit.returnPressed.connect(send_next_value)

worker.start()
napari.run()
