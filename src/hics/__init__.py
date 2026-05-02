"""hics: Hierarchical Coordinate Systems."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("hics")
except PackageNotFoundError:
    # Package is not installed
    __version__ = "0.0.0-dev"


# Lazy-loading the core class to avoid circular triggers
from xrench.units import ureg

from .config import HICSLogger
from .hics import GLOBAL_CS, HCS

__all__ = ["HCS", "GLOBAL_CS", "ureg", "HICSLogger"]
