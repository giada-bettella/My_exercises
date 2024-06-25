# exercise 02

# print out cities in France with intersect

from pyqgis_scripting_ext.core import *

folder = "/Users/giadina/Desktop/UNIBZ ⛰️/Geomatic and evironmental impact assessment /Advanced geomatics/My_exercises"

geopackagePath = folder + "/data/reduced_ne.gpkg"
countriesName = 'ne_50m_admin_0_countries'
citiesName = 'ne_50m_populated_places'

# load the layers
countriesLayer = HVectorLayer.open(geopackagePath, countriesName)
citiesLayer = HVectorLayer.open(geopackagePath, citiesName)

# countries
nameIndexCountries = countriesLayer.field_index('NAME')
countriesFeatures = countriesLayer.features()

for feature in countriesFeatures:
    name = feature.attributes[nameIndexCountries]
    if name == 'France':
        countryGeometry = feature.geometry
        

# cities
nameIndexCities = citiesLayer.field_index('NAME')
citiesFeatures = citiesLayer.features()

# visualization:

crsHelper = HCrs()
crsHelper.from_srid(4326)
crsHelper.to_srid(3857)

canvas = HMapCanvas.new()

osm = HMap.get_osm_layer()
canvas.set_layers([osm])


countryGeometry3857 = crsHelper.transform(countryGeometry)
canvas.add_geometry(countryGeometry3857)


citiesInFrance = []

for feature in citiesFeatures:
    name = feature.attributes[nameIndexCities]
    cityGeometry = feature.geometry
    if countryGeometry.intersects(cityGeometry):
        citiesInFrance.append(name)
        canvas.add_geometry(crsHelper.transform(cityGeometry), 'blue')
        

canvas.set_extent(countryGeometry3857.bbox())
canvas.show()

# results
print('Cities in France:')
print(citiesInFrance)