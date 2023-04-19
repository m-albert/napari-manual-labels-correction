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
    process_only_current_2d_plane=dict(label='Process only visible 2D plane: '),
    # modify_in_place=dict(label='Modify labels in place: '),
    call_button="Rebuild labels",
)
def label_repair_magic_widget(
        viewer: 'napari.viewer.Viewer',
        label_layer: "napari.layers.Labels",
        process_only_current_2d_plane: bool=True,
        # modify_in_place: bool=True,
):
        # ) -> LayerDataTuple:

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

    input_labels = label_layer.data#.squeeze()

    if process_only_current_2d_plane:

      current_step = viewer.dims.current_step[:-2]
      curr_labels = input_labels[tuple(current_step)]

    else:
      
      curr_labels = input_labels

    processed_labels = _utils.process_labels(curr_labels.squeeze())

    if process_only_current_2d_plane:
       
      input_labels[tuple(current_step)] = processed_labels

    else:
       
      input_labels[:] = processed_labels

    label_layer.refresh()

    return

    # out_layers = []
    # out_layers.append((output_labels,
    #                    {'name': label_layer.name + '_rebuilt',
    #                     'scale': label_layer.scale,
    #                     },
    #                    'labels'))

    # return(out_layers)

