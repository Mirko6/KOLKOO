from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import shapefile

point = Point(0.5, 0.5)
polygon = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
print(polygon.contains(point))

polygons = []
sf = shapefile.Reader("slope_deformations_reference_polygons/reference_data_existing_landslides_polygons.shp")
shapes = sf.shapes()

shape = shapes[25]
print(shape.points)

for shape in shapes:
    polygons.append(Polygon(shape.points))

def is_in_polygon(x, y):
    point = Point(x, y)
    for polygon in polygons:
        if polygon.contains(point):
            return True
    return False
