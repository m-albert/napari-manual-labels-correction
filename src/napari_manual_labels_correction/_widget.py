"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

import numpy as np

from napari.utils import notifications
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


@magic_factory(
    label_layer=dict(label='Input Labels: '),
    shapes_layer=dict(label='Input Lines: '),
    call_button="Split labels",
)
def label_split_magic_widget(
        viewer: 'napari.viewer.Viewer',
        label_layer: "napari.layers.Labels",
        shapes_layer: "napari.layers.Shapes",
):
    """
    Split 2D labels
    """

    if shapes_layer is None:
      notifications.show_info('No lines drawn. Create (or select) a shapes layer and draw lines on it.')
      return

    if len(shapes_layer.data) == 0:
      notifications.show_info('No lines drawn. To split labels, draw lines on a shapes layer.')
      return

    if not np.all([st == 'line' for st in shapes_layer.shape_type]):
      raise ValueError('Shapes layer must contain only lines')

    input_labels = label_layer.data

    current_step = viewer.dims.current_step[:-2]
    curr_labels = input_labels[tuple(current_step)]

    
    masks = shapes_layer.to_masks()
    for iline, line in enumerate(shapes_layer.data):

      affected_labels = curr_labels[np.where(masks[iline][:curr_labels.shape[0], :curr_labels.shape[1]])]

      affected_labels_unique = np.unique(affected_labels[affected_labels>0])
      # if len(affected_labels_unique) > 1:
      #   notifications.show_error('Lines must split only one label')
      #   return
            
      line_endpoints = np.array([
         shapes_layer.world_to_data(shapes_layer.data[iline][i])
         for i in range(2)])
      
      # compute normal vector to line
      line_vector = line_endpoints[1] - line_endpoints[0]
      line_vector /= np.linalg.norm(line_vector)
      normal_vector = np.array([-line_vector[1], line_vector[0]])

      for affected_label in affected_labels_unique:
      
        label_coords = np.where(curr_labels == affected_label)
        label_coords = np.array(label_coords).T

        # separate label_coords into two sets
        # based on which side of the line they are on
        # compute dot product of label_coords with normal vector

        dot_products = np.dot(label_coords - line_endpoints[0], normal_vector)

        # label_coords on one side of the line will have positive dot product
        # and those on the other side will have negative dot product

        new_label = np.max(curr_labels) + 1

        curr_labels[tuple(label_coords[dot_products > 0].T)] = new_label
      
    shapes_layer.data = []

    label_layer.refresh()

    return
