import numpy as np

from napari_manual_labels_correction import label_repair_magic_widget


def test_label_repair_magic_widget(make_napari_viewer, capsys):
    viewer = make_napari_viewer()
    layer = viewer.add_labels(np.random.randint(0, 100, (10, 10)))

    # this time, our widget will be a MagicFactory or FunctionGui instance
    my_widget = label_repair_magic_widget()

    # if we "call" this object, it'll execute our function
    my_widget(viewer.layers[0])

    # read captured output and check that it's as we expected
    captured = capsys.readouterr()
    assert captured.out == f"you have selected {layer}\n"
