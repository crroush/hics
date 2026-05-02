"""HICS geo downloader tests."""

import pytest
import xarray as xr

from hics import HCS, ureg
from hics.datatypes import _POSITION_COORD_DICT, _POSITION_DIM
from hics.geo.config import DEM_SETTINGS
from hics.geo.dem import DEM
from hics.geo.downloader import DEM_CATALOG, GEOTIFF_INDEX


def test_download(tmp_path):
    DEM_SETTINGS.DEM_FOLDER = tmp_path
    GEOTIFF_INDEX.cache_dir = tmp_path

    truth = xr.DataArray(
        [-1288677.85726808, -4720141.82855096, 4080318.25299769] * ureg.meter,
        dims=[_POSITION_DIM],
        coords=_POSITION_COORD_DICT,
    )
    # Use a coarse dataset
    DEM.dem_asset = DEM_CATALOG.COP90
    cs_boulder = HCS.from_crs(
        (40.015 * ureg.degree, -105.270556 * ureg.degree, 20 * ureg.m), hagl=True
    )
    xr.testing.assert_allclose(cs_boulder.global_position, truth)
