import numpy as np

from napari_manual_labels_correction import _utils

def test_label_contiguos():

    labels = np.zeros((5, 5), dtype=np.uint16)
    labels[0,0] = 1
    labels[2,2] = 3
    labels[3,3] = 99

    labels_contiguous = _utils.relabel_contiguous(labels)

    assert(labels[0,0] == 1)
    assert(labels[2, 2] == 2)
    assert(labels[3, 3] == 3)

    labels = np.randint(0, 100, size=(100, 100))
    labels_contiguous = _utils.relabel_contiguous(labels)
    labels_contiguous_2 = _utils.relabel_contiguous(labels_contiguous)

    assert(np.all(labels_contiguous == labels_contiguous_2))


def test_reassign_connected_components_per_label():

    labels = np.randint(0, 100, size=(100, 100))
    labels_reassigned = _utils.test_reassign_connected_components_per_label(labels)
    labels_reassigned_2 = _utils.test_reassign_connected_components_per_label(labels_reassigned)

    assert(np.all(labels_reassigned == labels_reassigned_2))


