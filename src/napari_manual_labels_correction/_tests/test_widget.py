import numpy as np

from napari_manual_labels_correction import label_repair_magic_widget


def test_label_repair_magic_widget(make_napari_viewer):
    viewer = make_napari_viewer()
    layer = viewer.add_labels(np.random.randint(0, 100, (10, 10)))

    # this time, our widget will be a MagicFactory or FunctionGui instance
    my_widget = label_repair_magic_widget()

    # if we "call" this object, it'll execute our function
    out_layers = my_widget(viewer.layers[0])
