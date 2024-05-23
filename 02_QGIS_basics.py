# Exercise 02
path = "/Users/giadina/Desktop/UNIBZ ⛰️/Geomatic and evironmental impact assessment /Advanced geomatics/Data/stations.txt"

with open(path, 'r') as file:
       lines = file.readlines()

countryCode = []
points = []

for line in lines[1:]:
    lineSplit = line.split(",")
    
    country = lineSplit[2]
    countryCode.append(country)
    
    lat = lineSplit[3].strip("+")
    lon = lineSplit[4]. strip("+")
    
    latSplit = lat.split(":")
    lonSplit = lon.split(":")
    
    convLat1 = float(latSplit[1])/60
    convLat2 = float(latSplit[2])/3600
    convLon1 = float(lonSplit[1])/60
    convLon2 = float(lonSplit[2])/3600
    
    latFinal = float(latSplit[0]) + convLat1 + convLat2
    lonFinal = float(lonSplit[0]) + convLon1 + convLon2
    
    point = HPoint(lonFinal, latFinal)
    points.append(point)

print(points[0])
    
canvas = HMapCanvas()

for point in points:
    canvas.add_geometry(point, "red", 1)

bounds = [0, 0, 180, 90]
canvas.set_extent(bounds)
canvas.show()

uniqueValues = set(countryCode)

for item in uniqueValues:
    statNum = countryCode.count(item)
    print(f"{item}: {statNum}")