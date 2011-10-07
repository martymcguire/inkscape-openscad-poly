from math import cos, sin, radians
import pprint

class Entity:
	def make_poly(self,context):
		#raise NotImplementedError()
		return "NIE"

class Path(Entity):
	def __str__(self):
		return "Polyline consisting of %d segments." % len(self.segments)

	def make_poly(self,context):
		"Emit polygon dict with id, points, paths"
		context.add_poly(self.id, self.points, self.paths)
