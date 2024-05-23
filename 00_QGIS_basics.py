# Exercise 00

from pyqgis_scripting_ext.core import *

path = "/Users/giadina/Desktop/UNIBZ ⛰️/Geomatic and evironmental impact assessment /Advanced geomatics/Lecture_3/02_exe0_geometries.csv"

with open(path, "r") as file:
    readLines = file.readlines()
    
    
points = []
lines = []
polygons = []
for line in readLines:
    line = line.strip()
    #print(line)
    
    split = line.split(";")
    gtype = split[0]
    coords = split[1]
    num = split[2]
    
    if gtype == "point":
        coordSplit = coords.split(",")
        longitude = float(coordSplit[0])
        latitude = float(coordSplit[1])
        point = HPoint(longitude, latitude)
        print(point)
        points.append(point)
    elif gtype == "line":
        coordSplit = coords.split(" ")
        pointList = []
        for coordString in coordSplit:
            split = coordString.split(",")
            longitude = float(split[0])
            latitude = float(split[1])
            pointList.append
            pointList.append([longitude, latitude])
        line = HLineString.fromCoords(pointList)
        lines.append(line)
    elif gtype == "polygon":
        coordSplit = coords.split(" ")
        pointList = []
        for coordString in coordSplit:
            split = coordString.split(",")
            longitude = float(split[0])
            latitude = float(split[1])
            pointList.append
            pointList.append([longitude, latitude])
        polygon = HPolygon.fromCoords(pointList)
        polygons.append(polygon)
        
        
canvas = HMapCanvas()

for point in points:
    canvas.add_geometry(point, "magenta", 50)

for line in lines:
    canvas.add_geometry(line, "blue", 3)
    
for polygon in polygons:
    canvas.add_geometry(polygon, "red", 1)
    
bounds = [0, 0, 50, 50]
canvas.set_extent(bounds)
canvas.show()