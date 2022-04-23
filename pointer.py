from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import shapefile

polygons = []
sf = shapefile.Reader("slope_deformations_reference_polygons/reference_data_existing_landslides_polygons.shp")
shapes = sf.shapes()

for shape in shapes:
    polygons.append(Polygon(shape.points))

def is_in_polygon(x, y):
    point = Point(x, y)
    for polygon in polygons:
        if polygon.contains(point):
            return True
    return False
