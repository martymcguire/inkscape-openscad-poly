"""
Contributors:
Copyright (c) 2016 Benedict Endemann
"""

class OSCADPolyContext:
    def __init__(self, svg_file):
        self.file = svg_file
        self.polygons = []

    def generate(self):
        # generate list of all modules at top for easy control
        for polygon in self.polygons:
            if polygon['color']:
                print "color([{:0.4f}, {:0.4f}, {:0.4f}, {:0.4f}]) {}();".format(
                    polygon['color'][0],
                    polygon['color'][1],
                    polygon['color'][2],
                    polygon['color'][3],
                    polygon['id'])
            else:
                print "{}();".format(polygon['id'])

        # generate actual modules from polygons
        for polygon in self.polygons:
            print
            print "module {}()".format(polygon['id'])
            print "    polygon("
            print "        points="
            print "            {},".format(polygon['points'])
            print "        paths="
            print "            {}".format(polygon['paths'])
            print "    );"

    def add_poly(self, poly_id, points, paths, color = None):
        shortened_points = [[round(x, 3),round(y, 3)] for x, y in points]
        self.polygons.append({ 'id': poly_id, 'points':shortened_points, 'paths':paths, 'color':color})
