import numpy as np

from napari_manual_labels_correction import (
    label_repair_magic_widget,
    label_split_magic_widget,
)


def test_label_repair_magic_widget(make_napari_viewer):
    viewer = make_napari_viewer()
    label_layer = viewer.add_labels(np.random.randint(0, 100, (10, 10)))

    # this time, our widget will be a MagicFactory or FunctionGui instance
    my_widget = label_repair_magic_widget()

    # if we "call" this object, it'll execute our function
    out_layers = my_widget(viewer, viewer.layers[0])


def test_label_split_magic_widget(make_napari_viewer):
    viewer = make_napari_viewer()

    # build simple example label array

    label_array = np.zeros((10, 10), dtype=int)
    label_array[2:8, 2:8] = 1

    label_layer = viewer.add_labels(label_array)

    shapes_layer = viewer.add_shapes([[0, 0], [9, 9]], shape_type='line')

    # this time, our widget will be a MagicFactory or FunctionGui instance
    my_widget = label_split_magic_widget()

    # if we "call" this object, it'll execute our function
    out_layers = my_widget(viewer, label_layer, shapes_layer)
