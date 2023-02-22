"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

import numpy as np

from napari.types import LayerDataTuple
from magicgui import magic_factory

from napari_manual_labels_correction import _utils

if TYPE_CHECKING:
    import napari


@magic_factory(
    label_layer=dict(label='Input Labels: '),
    call_button="Rebuild labels",
)
def label_repair_magic_widget(
        label_layer: "napari.layers.Labels",
        ) -> LayerDataTuple:

    """
    Rebuild labels after manual correction using napari's built-in
    labels manipulation tools.

    We assume the following to be true about valid labels:
    - labels are contiguous in space. E.g. for a given label
      there is only once connected component in the image

    This function will attempt to rebuild labels such that the following
    correction steps will be included in a valid output label map:
    - under-segmentation: objects have been split by drawing a line
      between subsets of the original label
    - additional objects: new objects have been added to the label
      map, using labels that are not necessarily unique
    - output labels are contiguous in label space
    """

    input_labels = label_layer.data

    # relabel contiguously
    curr_labels = _utils.relabel_contiguous(input_labels)

    # loop through labels and find connected components
    curr_labels = _utils.reassign_connected_components_per_label(curr_labels)
    
    # relabel contiguously again
    curr_labels = _utils.relabel_contiguous(curr_labels)

    out_layers = []
    out_layers.append((curr_labels,
                       {'name': label_layer.name + '_rebuilt'}, 'labels'))

    return(out_layers)

