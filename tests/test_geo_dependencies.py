"""Tests for geospatial dependency guidance."""

from hics.geo import geospatial_install_message


def test_geospatial_install_message_explains_gdal_version_matching():
    message = geospatial_install_message()

    assert "GDAL's Python bindings" in message
    assert "gdal-config --version" in message
    assert "gdal==$(gdal-config --version)" in message
