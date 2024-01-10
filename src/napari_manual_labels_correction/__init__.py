
try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"
from ._sample_data import make_sample_data
from ._widget import label_repair_magic_widget, label_split_magic_widget

__all__ = (
    "make_sample_data",
    "label_repair_magic_widget",
    "label_split_magic_widget",
)
