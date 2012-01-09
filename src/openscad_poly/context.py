from math import *
import sys

class pfloat(float):
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
      newpoints = [[pfloat(x), pfloat(y)] for x, y in points]
      self.polygons.append({ 'id': id, 'points':newpoints, 'paths':paths})
