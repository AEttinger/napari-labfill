"""
This module is an example of a barebones QWidget plugin for napari

It implements the ``napari_experimental_provide_dock_widget`` hook specification.
see: https://napari.org/docs/dev/plugins/hook_specifications.html

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

from enum import Enum
import numpy as np
from napari_plugin_engine import napari_hook_implementation

if TYPE_CHECKING:
    import napari
from magicgui.widgets import PushButton
from skimage.segmentation import flood, flood_fill
from skimage.filters import gaussian


@napari_hook_implementation
def napari_experimental_provide_function():
    # we can return a single function
    # or a tuple of (function, magicgui_options)
    # or a list of multiple functions with or without options, as shown here:
    return fill_connected


def fill_connected(data: "napari.types.ImageData", threshold: int, sigma: float, connected: int) -> "napari.types.LabelsData":
    img_gauss = gaussian(data, sigma=sigma, preserve_range=True)
    return flood(img_gauss, tolerance=threshold, connectivity=connected).astype(int)