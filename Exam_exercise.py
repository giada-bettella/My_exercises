# ESAM EXERCISE GROUP 3

from pyqgis_scripting_ext.core import *

folder = "/Users/giadina/Desktop/UNIBZ ⛰️/Geomatic and evironmental impact assessment /Advanced geomatics/My_exercises/"
data_folder = folder + "data/"

geopackagePath = data_folder + "reduced_ne.gpkg"
countriesName = "ne_50m_admin_0_countries"
countriesLayer = HVectorLayer.open(geopackagePath, countriesName)
countriesLayer.subset_filter("NAME = 'Italy' OR NAME = 'Germany'" )

#remove layer from map
HMap.remove_layers_by_name(['OpenStreetMap', 'ne_50m_admin_0_countries', 'Battles', 'Country border'])

# import the http requests library to get stuff from the internet
import requests
# import the url parsing library to urlencode the query 
import urllib.parse
# define the query to launch
endpointUrl = "https://query.wikidata.org/sparql?query=";
# define the query to launch
query = """
SELECT ?label ?coord ?subj ?year 
WHERE
{
?subj wdt:P31 wd:Q178561 .
{?subj wdt:P17 wd:Q38} UNION {?subj wdt:P17 wd:Q183}.
?subj wdt:P625 ?coord .
OPTIONAL {?subj wdt:P580 ?d1}
OPTIONAL {?subj wdt:P585 ?d2}
OPTIONAL {?subj wdt:P582 ?d3} BIND(IF(!BOUND(?d1),(IF(!BOUND(?d2),?d3,?d2)),?d1) as ?date) BIND(YEAR(?date) as ?year)
?subj rdfs:label ?label filter (lang(?label) = "en")
}
"""

# URL encode the query string
encoded_query = urllib.parse.quote(query)

# prepare the final url
url = f"{endpointUrl}{encoded_query}&format=json"

# run the query online and get the produced result as a dictionary
r = requests.get(url)
result = r.json()

# print(result)
# -------------------------------------------------------------------------

# print(len(result))
# print(result['results']['bindings']

# add OSM to map
osm = HMap.get_osm_layer()
HMap.add_layer(osm)

# CRS TRANSFORMATION
crsHelper = HCrs()
crsHelper.from_srid(4326)
crsHelper.to_srid(3857)

nameIndexCountries = countriesLayer.field_index('NAME')
countriesFeatures = countriesLayer.features()

# ADD THE COUNTRIES BORDER
fields1 = {
    "name": "String"}

countriesLayer3857 = HVectorLayer.new("Country border", "MultiPolygon", "EPSG:3857", fields1)

for feature in countriesFeatures:
        countriesName = feature.attributes[nameIndexCountries]
        countriesGeometry = feature.geometry
        countries3857 = crsHelper.transform(countriesGeometry)
        countriesLayer3857.add_feature(countries3857, [countriesName])

# print(countriesFeatures[0].geometry)

# CREATE A SCHEMA
fields2 = {
    "year": "Interger",
     "name": "String"}

# battlesLayer = HVectorLayer.new("Battles", "Point", "EPSG:4326", fields)
battlesLayer = HVectorLayer.new("Battles", "Point", "EPSG:3857", fields2)

# print name - year - coords
# print(result['results']['bindings'][0])

counterItaly = 0
counterGermany = 0

# SELECT DATA THAT WE NEED
for item in result['results']['bindings']:
    name = item['label']['value']
    if "year" in item:
        year = int(item['year']['value'])
    else:
        year = None
    coord = item['coord']['value'].strip('Point(').strip(')').split(' ')
    lon = float(coord[0])
    lat = float(coord[1])
    location = HPoint(lon, lat)
    location3857 = crsHelper.transform(location)
 
# CHECK IF POINTS ARE IN ITALY OR GERMANY 
    for feature in countriesFeatures:
        countriesName = feature.attributes[nameIndexCountries]
        countriesGeometry = feature.geometry
        
        if location.intersects(countriesGeometry):
            battlesLayer.add_feature((location3857), [year, name])
            
# COUNTRY WITH MORE BATTLES
            if year and 0 <= year <= 1000:
                if countriesName == "Italy":
                    counterItaly += 1
                else:
                    counterGermany += 1

    # print(name, year, coords)
    
print(counterItaly, counterGermany)
    
# CREATE GPKG
path = folder + "battles.gpkg"
error = battlesLayer.dump_to_gpkg(path, overwrite = True)

if error:
    print(error)

# COUNTRIES STYLE
countriesStyle = HFill('128, 128, 128, 70') + HStroke('black', 0.5)
countriesLayer3857.set_style(countriesStyle)

# BATTLES STYLE
ranges = [
    [float('-inf'), 0],
    [1, 1000],
    [1001, 1500],
    [1501, float('inf')]
]

styles = [
    HMarker("circle", 2) + HFill("red") + HStroke("black", 0.1),
    HMarker("circle", 2) + HFill("blue") + HStroke("black", 0.1),
    HMarker("circle", 2) + HFill("green") + HStroke("black", 0.1),
    HMarker("circle", 2) + HFill("orange") + HStroke("black", 0.1)
]

# field = "if(year >= 0 and year <= 1000, NAME,'')"
# labelProperties3 = {
#     "font": "Times New Roman",
#     "color": "black",
#     "size": 10,
#     "field": field,
#     "xoffset": 0,
#     "yoffset": -8
# }

# pointStyle += HLabel(**labelProperties3) + HHalo("white", 2)
# battlesLayer.set_graduated_style('year', ranges, styles, pointStyle)
battlesLayer.set_graduated_style('year', ranges, styles)

# ADD LAYER TO THE MAP
HMap.add_layer(countriesLayer3857)
HMap.add_layer(battlesLayer)

# CREATE THE LAYOUT PDF
printer = HPrinter(iface)           #create new layout
print(countriesLayer3857.bbox())
#bbox = [652056.0915304051, 4395684.818450607, 2057834.2782922578, 7373274.750832028]

mapProperties = {
    "x": 5,
    "y": 5,
    "width": 200,
    "height": 200,
    "extent": [642056, 4295684, 2157834, 7473274],
    "frame": True
    }
printer.add_map(**mapProperties)

labelProperties = {
    "x": 210,
    "y": 5,
    "text": "HISTORY OF BATTLES\nIN ITALY AND GERMANY",
    "font": "Times New Roman",
    "font_size": 18,
    "bold": True,
    "italic": False
}
printer.add_label(**labelProperties)

scalebarProperties = {
    "x": 8,
    "y": 190,
    "units": "km",
    "segments": 4,
    "unit_per_segment": 250,
    "style": "Double Box",
    "font_size": 8,
    "font": "Times New Roman"
}
printer.add_scalebar(**scalebarProperties)

legendProperties = {
    "x": 210,
    "y": 148,
    "width": 30,
    "height": 100,
    "max_symbol_size": 3
}
printer.add_legend(**legendProperties)

labelProperties2 = {
    "x": 210,
    "y": 50,
    "text": f"Battles between 0 and 1000:\nItaly: {counterItaly}\nGermany: {counterGermany}",
    "font": "Times New Roman",
    "font_size": 15,
    "bold": True,
    "italic": False
}
printer.add_label(**labelProperties2)

# PRINT THE PDF
outputPdf = f"{folder}final_map.pdf"
printer.dump_to_pdf(outputPdf)


