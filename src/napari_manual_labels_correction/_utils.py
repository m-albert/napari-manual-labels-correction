import numpy as np
from scipy import ndimage


def relabel_contiguous(labels):
    """
    Relabels a label map such that the output labels are contiguous in label space.
    """
    # find unique labels
    unique_labels = np.unique(labels)
    # relabel
    relabel_map = {label: i for i, label in enumerate(unique_labels)}
    relabeled_labels = np.copy(labels)
    for label in unique_labels:
        relabeled_labels[labels == label] = relabel_map[label]
    return relabeled_labels


def reassign_connected_components_per_label(labels):
    """
    Find connected components for each label in a label map.
    """

    output_labels = np.copy(labels)

    # find unique labels
    unique_labels = np.unique(labels)

    # find connected components
    curr_max_label = np.max(unique_labels)

    label_slices = ndimage.find_objects(labels,
                                        max_label=curr_max_label)

    for label_minus_one, label_slice in\
        zip(unique_labels, label_slices):
        if label_slice is None:
            continue

        label = label_minus_one + 1

        label_mask = labels[label_slice] == label

        # obtain connected components for current label
        label_labels, N_sub = ndimage.label(label_mask)
        if N_sub == 1: # only one CC, don't do anything
            continue
        
        # assign new labels to output labels
        output_labels[label_slice][label_mask] = \
            label_labels[label_mask] + curr_max_label

        # keep track of current max label
        curr_max_label += N_sub

    return output_labels


def process_labels(labels):
    """
    Perform full correction
    """

    # relabel contiguously
    labels = relabel_contiguous(labels)

    # loop through labels and find connected components
    labels = reassign_connected_components_per_label(labels)
    
    # relabel contiguously again
    labels = relabel_contiguous(labels)

    return labels


if __name__ == "__main__":

    labels = np.array([0, 1, 1, 0, 3, 3, 0, 3, 3, 0])

    # labels = np.random.randint(0, 10, size=(10, 10))

    labelsc = relabel_contiguous(labels)
    labelscr = reassign_connected_components_per_label(labelsc)
