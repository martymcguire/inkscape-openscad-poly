"""
Contributors:
Copyright (c) 2016 Benedict Endemann
Copyright (c) 2011 Marty McGuire
"""


class Entity(object):
    def __init__(self):
        pass

    def make_poly(self, context):
        raise NotImplementedError()

class Path(Entity):
    def __init__(self):
        super(Path, self).__init__()
        self.id       = ''
        self.segments = []
        self.points   = []
        self.paths    = []
        self.color    = None

    def __str__(self):
        return "Polyline consisting of {} segments.".format(len(self.segments))

    def make_poly(self, context):
        """
        Emit polygon dict with id, points, paths
        """
        context.add_poly(self.id,
                         [[round(n, 5) for n in p] for p in self.points],
                         self.paths, self.color)
