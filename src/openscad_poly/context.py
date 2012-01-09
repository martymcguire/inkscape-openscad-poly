from math import *
import sys

class shorter_float(float):
    """A float which returns only 3 digits after the decimal"""
    def __repr__(self):
      return "%0.3f" % self

class OSCADPolyContext:
    def __init__(self, file):
      self.file = file
      
      self.polygons = []

    def generate(self):
      for polygon in self.polygons:
        print "module %s() {" % polygon['id']
        print "  polygon(points="
        print("    " + str(polygon['points']))
        print "    , paths="
        print("    " + str(polygon['paths']))
        print "    );}"

    def add_poly(self, id, points, paths):
      shortened_points = [[shorter_float(x), shorter_float(y)] for x, y in points]
      self.polygons.append({ 'id': id, 'points':shortened_points, 'paths':paths})
