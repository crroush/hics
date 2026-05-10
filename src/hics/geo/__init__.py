"""Geospatial dependency checks for hics."""

from __future__ import annotations

import importlib.util
import platform
import shutil
import subprocess

_GDAL_INSTALL_HELP = """hics geospatial features require GDAL's Python bindings (`osgeo`).
The bindings must match the system `libgdal` version; installing an arbitrary
`gdal` wheel from PyPI often fails or creates an ABI mismatch.

On Ubuntu, install system GDAL first, then install the matching Python bindings:

    sudo apt-get update
    sudo apt-get install -y gdal-bin libgdal-dev libspatialindex-dev
    uv pip install "gdal==$(gdal-config --version)"

On Windows or macOS, use a geospatial distribution such as conda-forge, or install
GDAL with your platform package manager first and then install Python bindings
that match that GDAL version.

If you are not using uv, run the equivalent command in the active environment:

    python -m pip install "gdal==$(gdal-config --version)"
"""

_REQUIRED_GEO_MODULES = {
    "pyproj": "pyproj",
    "rasterio": "rasterio",
    "rioxarray": "rioxarray",
    "osgeo": "GDAL Python bindings (`osgeo`)",
}


def missing_geospatial_dependencies() -> list[str]:
    """Return missing Python modules needed for geospatial features."""
    return [
        description
        for module, description in _REQUIRED_GEO_MODULES.items()
        if importlib.util.find_spec(module) is None
    ]


def _system_gdal_version() -> str | None:
    """Return the system GDAL version reported by gdal-config, if available."""
    if shutil.which("gdal-config") is None:
        return None
    result = subprocess.run(
        ["gdal-config", "--version"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def geospatial_install_message() -> str:
    """Return actionable installation guidance for geospatial dependencies."""
    missing = missing_geospatial_dependencies()
    message = _GDAL_INSTALL_HELP
    if missing:
        message = f"Missing geospatial dependencies: {', '.join(missing)}.\n\n{message}"

    system_gdal = _system_gdal_version()
    if system_gdal is not None:
        message += f"\nDetected system GDAL version: {system_gdal}.\n"
    else:
        message += f"\nNo gdal-config executable was detected on {platform.system()}.\n"

    return message


def require_geospatial_dependencies() -> None:
    """Raise an actionable error if geospatial dependencies are not installed."""
    if missing_geospatial_dependencies():
        raise ImportError(geospatial_install_message())


HAS_GEO_DEPS = not missing_geospatial_dependencies()
