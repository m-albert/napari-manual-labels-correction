"""
This module is an example of a barebones sample data provider for napari.

It implements the "sample data" specification.
see: https://napari.org/stable/plugins/guides.html?#sample-data

Replace code below according to your needs.
"""
from __future__ import annotations

import numpy as np

def make_sample_data():
    """Generates an image"""
    # Return list of tuples
    # [(data1, add_image_kwargs1), (data2, add_image_kwargs2)]
    # Check the documentation for more information about the
    # add_image_kwargs
    # https://napari.org/stable/api/napari.Viewer.html#napari.Viewer.add_image

    labels = np.zeros((100, 100), dtype=np.uint16)

    labels[10:20, 10: 90] = 1
    labels[30:40, 10: 90] = 1

    labels[50:60, 10: 90] = 3
    labels[50:60, 50] = 0

    labels[70:80, 10: 90] = 4

    return [(labels, {}, 'labels')]
