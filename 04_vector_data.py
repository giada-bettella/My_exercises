# Exercise 04

from pyqgis_scripting_ext.core import *

folder = "/Users/giadina/Desktop/UNIBZ ⛰️/Geomatic and evironmental impact assessment /Advanced geomatics/My_exercises"
geopackagePath = f"{folder}/natural_earth_vector/packages/natural_earth_vector.gpkg"
countriesName = "ne_50m_admin_0_countries"

countriesLayer = HVectorLayer.open(geopackagePath, countriesName)

ranges = [
    [80000000, float('inf')],
    [1000000, 80000000],
    [float('inf'), 1000000]
]

styles = [
    HFill("255, 0, 0, 70"),
    HFill("0, 255, 0, 70"),
    HFill("0, 0, 255, 70")
] 

labelStyle = HLabel("POP_EST") + HHalo()

countriesLayer.set_graduated_style("POP_EST", ranges, styles, labelStyle)
HMap.add_layer(countriesLayer)


