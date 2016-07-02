class ShorterFloat(float):
    """A float which returns only 3 digits after the decimal"""
    def __repr__(self):
        return "%0.3f" % self

class OSCADPolyContext:
    def __init__(self, svg_file):
        self.file = svg_file
        self.polygons = []

    def generate(self):
        for polygon in self.polygons:
            print "module %s() {" % polygon['id']
            print "  polygon(points="
            print("    " + str(polygon['points']))
            print "    , paths="
            print("    " + str(polygon['paths']))
            print "    );}"

    def add_poly(self, poly_id, points, paths):
        shortened_points = [[ShorterFloat(x), ShorterFloat(y)] for x, y in points]
        self.polygons.append({ 'id': poly_id, 'points':shortened_points, 'paths':paths})
