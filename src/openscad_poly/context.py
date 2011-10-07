from math import *
import sys

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
      self.polygons.append({ 'id': id, 'points':points, 'paths':paths})

