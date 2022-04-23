from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import shapefile

polygons = []
sf = shapefile.Reader("slope_deformations_reference_polygons/reference_data_existing_landslides_polygons.shp")
shapes = sf.shapes()
rectangles = []

for shape in shapes:
    polygons.append(Polygon(shape.points))
    rectangles.append(shape.bbox)

def is_in_optimised(x, y):
    for i in range(len(polygons)):
        rectangle = rectangles[i]
        bottom_left_x, bottom_left_y, upper_right_x, upper_right_y = rectangle[0], rectangle[1], rectangle[2], rectangle[3]
        if x >= bottom_left_x and x <= upper_right_x and y >= bottom_left_y and y <= upper_right_y:
            polygon = polygons[i]
            if polygon.contains(Point(x, y)):
                return True

    return False

def is_in_polygon(x, y):
    point = Point(x, y)
    for polygon in polygons:
        if polygon.contains(point):
            return True
    return False
