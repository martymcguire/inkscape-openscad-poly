import inkex, cubicsuperpath, simplepath, simplestyle, cspsubdiv
from simpletransform import applyTransformToPath, parseTransform, composeTransform
from bezmisc import beziersplitatt
import entities

def parse_length_with_units(string):
    """
    Parse an SVG value which may or may not have units attached
    This version is greatly simplified in that it only allows: no units,
    units of px, units of mm, and units of %.  Everything else,
    it returns None for.
    There is a more general routine to consider in scour.py if more
    generality is ever needed.
    """

    u = 'px'
    s = string.strip()
    if s[-2:] == 'px':
        s = s[:-2]
    elif s[-2:] == 'mm':
        u = 'mm'
        s = s[:-2]
    elif s[-1:] == '%':
        u = '%'
        s = s[:-1]
    try:
        v = float( s )
    except ValueError:
        return None, None
    return v, u

def subdivide_cubic_path(sp, flat, i=1):
    """
    Break up a bezier curve into smaller curves, each of which
    is approximately a straight line within a given tolerance
    (the "smoothness" defined by [flat]).

    This is a modified version of cspsubdiv.cspsubdiv(). I rewrote the recursive
    call because it caused recursion-depth errors on complicated line segments.
    """

    b = None
    while True:
        while True:
            if i >= len( sp ):
                return

            p0 = sp[i - 1][1]
            p1 = sp[i - 1][2]
            p2 = sp[i][0]
            p3 = sp[i][1]

            b = ( p0, p1, p2, p3 )

            if cspsubdiv.maxdist( b ) > flat:
                break

            i += 1

        if b is not None:
            one, two = beziersplitatt( b, 0.5 )
            sp[i - 1][2] = one[1]
            sp[i][0] = two[2]
            p = [one[2], one[3], two[1]]
            sp[i:1] = [p]

class SvgIgnoredEntity(entities.Path):
    def __init__(self):
        super(SvgIgnoredEntity, self).__init__()
        self.tag = ''

    def load(self, node, mat):
        self.tag = node.tag

    def __str__(self):
        return "Ignored '%s' tag" % self.tag

    def make_poly(self, context):
        # Entity should be ignored, so return nothing
        return

class SvgPath(entities.Path):
    def load(self, node, mat):
        self.id = node.get('id')
        d = node.get('d')
        if len(simplepath.parsePath(d)) == 0:
            return
        p = cubicsuperpath.parsePath(d)
        applyTransformToPath(mat, p)

        # p is now a list of lists of cubic beziers [ctrl p1, ctrl p2, endpoint]
        # where the start-point is the last point in the previous segment
        self.points = []
        self.paths = []
        for sp in p:
            path = []
            subdivide_cubic_path(sp, 0.2)  # TODO: smoothness preference
            for csp in sp:
                point = [csp[1][0], csp[1][1]]
                if point not in self.points:
                    self.points.append(point)
                path.append(self.points.index(point))
            self.paths.append(path)

    @staticmethod
    def new_path_from_node(node):
        newpath = inkex.etree.Element(inkex.addNS('path', 'svg'))
        newpath.set('id', node.get('id'))
        s = node.get('style')
        if s:
            newpath.set('style', s)
        t = node.get('transform')
        if t:
            newpath.set('transform', t)
        return newpath

class SvgRect(SvgPath):
    def load(self, node, mat):
        newpath = self.new_path_from_node(node)
        x = float(node.get('x'))
        y = float(node.get('y'))
        w = float(node.get('width'))
        h = float(node.get('height'))
        a = [
            ['M ',  [x, y] ],
            [' l ', [w, 0] ],
            [' l ', [0, h] ],
            [' l ', [-w, 0]],
            [' Z',  []     ]
        ]
        newpath.set('d', simplepath.formatPath(a))
        SvgPath.load(self, newpath, mat)

class SvgLine(SvgPath):
    def load(self, node, mat):
        newpath = self.new_path_from_node(node)
        x1 = float(node.get('x1'))
        y1 = float(node.get('y1'))
        x2 = float(node.get('x2'))
        y2 = float(node.get('y2'))
        a = [
            ['M ',  [x1, y1]],
            [' L ', [x2, y2]]
        ]
        newpath.set('d', simplepath.formatPath(a))
        SvgPath.load(self, newpath, mat)

class SvgPolyLine(SvgPath):
    def load(self, node, mat):
        newpath = self.new_path_from_node(node)
        pl = node.get('points', '').strip()
        if pl == '':
            return
        pa = pl.split()
        if not len(pa):
            return

        d = "M " + pa[0]
        for i in range(1, len(pa)):
            d += " L " + pa[i]
        newpath.set('d', d)
        SvgPath.load(self, newpath, mat)

class SvgEllipse(SvgPath):
    def load(self, node, mat):
        rx = float(node.get('rx', '0'))
        ry = float(node.get('ry', '0'))
        SvgPath.load(self, self.make_ellipse_path(rx, ry, node), mat)

    def make_ellipse_path(self, rx, ry, node):
        if rx == 0 or ry == 0:
            return None
        cx = float(node.get('cx', '0'))
        cy = float(node.get('cy', '0'))
        x1 = cx - rx
        x2 = cx + rx
        d = 'M %f,%f ' % (x1, cy) + \
            'A %f,%f ' % (rx, ry) + \
            '0 1 0 %f, %f ' % (x2, cy) + \
            'A %f,%f ' % (rx, ry) + \
            '0 1 0 %f,%f' % (x1, cy)
        newpath = self.new_path_from_node(node)
        newpath.set('d', d)
        return newpath

class SvgCircle(SvgEllipse):
    def load(self, node, mat):
        rx = float(node.get('r', '0'))
        SvgPath.load(self, self.make_ellipse_path(rx, rx, node), mat)

class SvgText(SvgIgnoredEntity):
    def load(self, node, mat):
        inkex.errormsg('Warning: unable to draw text. please convert it to a path first.')
        SvgIgnoredEntity.load(self, node, mat)


class SvgParser(object):
    entity_map = {
        'path': SvgPath,
        'rect': SvgRect,
        'line': SvgLine,
        'polyline': SvgPolyLine,
        'polygon': SvgPolyLine,
        'circle': SvgCircle,
        'ellipse': SvgEllipse,
        'pattern': SvgIgnoredEntity,
        'metadata': SvgIgnoredEntity,
        'defs': SvgIgnoredEntity,
        'desc': SvgIgnoredEntity,
        'eggbot': SvgIgnoredEntity,
        ('namedview', 'sodipodi'): SvgIgnoredEntity,
        'text': SvgText
    }

    def __init__(self, svg, pause_on_layer_change='false'):
        self.svg = svg
        self.pause_on_layer_change = pause_on_layer_change
        self.entities = []
        self.svgWidth = 0.0
        self.svgHeight = 0.0
        self.widthFactor  = 1.0
        self.heightFactor = 1.0

    def get_length(self, name, default = 354.0):
        """
        Get the <svg> attribute with name "name" and default value "default"
        Parse the attribute into a value and associated units. Then, accept
        no units (''), units of pixels ('px'), units of millimeter ('mm'),
        and units of percentage ('%').

        return length and factor for the named dimension
        """

        string = self.svg.get( name )

        if string:
            v, u = parse_length_with_units(string)
            if not v:
                # Couldn't parse the value
                return None

            elif ( u == '' ) or ( u == 'px' ):
                return [
                    v / default * 100.0,
                    100.0 / default
                ]

            elif u == 'mm':
                return [
                    v,
                    100.0 / default
                ]

            elif u == '%':
                # we do not know how big the viewport in pixels is (without iterating over every path TODO).
                # So we can't deliver the length and set it to "0" instead, so viewport starts at 0,0 in OpenSCAD
                return [
                    0,
                    v / 100.0
                ]

            else:
                # Unsupported units
                return None
        else:
            # Not specified; assume the default value
            return [
                default,
                100.0 / default
            ]

    def parse(self):
        [self.svgWidth,   self.widthFactor] = self.get_length('width')
        [self.svgHeight, self.heightFactor] = self.get_length('height')

        self.recursively_traverse_svg(self.svg,
            [
                [self.widthFactor,               0.0, -(self.svgWidth/2.0)],
                [            0.0, -self.heightFactor, (self.svgHeight/2.0)]
            ])

    def recursively_traverse_svg(self, node_list,
                                 mat_current = None,
                                 parent_visibility = 'visible'):
        """
        Recursively traverse the svg file to plot out all of the
        paths.  The function keeps track of the composite transformation
        that should be applied to each path.

        This function handles path, group, line, rect, polyline, polygon,
        circle, ellipse and use (clone) elements. Notable elements not
        handled include text.  Unhandled elements should be converted to
        paths in Inkscape.

        TODO: There's a lot of inlined code in the eggbot version of this
        that would benefit from the Entities method of dealing with things.
        """

        if not mat_current:
            mat_current = [
                [1.0,  0.0, 0.0],
                [0.0, -1.0, 0.0]
            ]

        for node in node_list:
            # Ignore invisible nodes
            v = node.get('visibility', parent_visibility)
            if v == 'inherit':
                v = parent_visibility
            if v == 'hidden' or v == 'collapse':
                pass

            # first apply the current matrix transform to this node's transform
            mat_new = composeTransform(mat_current, parseTransform(node.get("transform")))

            if node.tag == inkex.addNS('g', 'svg') or node.tag == 'g':
                self.recursively_traverse_svg(node, mat_new, parent_visibility = v)
            elif node.tag == inkex.addNS('use', 'svg') or node.tag == 'use':
                refid = node.get(inkex.addNS('href', 'xlink'))
                if refid:
                    # [1:] to ignore leading '#' in reference
                    path = '//*[@id="%s"]' % refid[1:]
                    refnode = node.xpath( path )
                    if refnode:
                        x = float(node.get('x', '0'))
                        y = float(node.get('y', '0'))
                        # Note: the transform has already been applied
                        if (x!=0) or (y!=0):
                            mat_new_2 = composeTransform(mat_new, parseTransform('translate(%f,%f)' % (x, y)))
                        else:
                            mat_new_2 = mat_new
                        v = node.get('visibility', v)
                        self.recursively_traverse_svg(refnode, mat_new_2, parent_visibility=v)
                    else:
                        pass
                else:
                    pass
            elif not isinstance(node.tag, basestring):
                pass
            else:
                entity = self.make_entity(node, mat_new)
                if entity is None:
                    inkex.errormsg('Warning: unable to draw object, please convert it to a path first.')

    def make_entity(self, node, mat):
        for nodetype in SvgParser.entity_map.keys():
            tag = nodetype
            ns = 'svg'
            if type(tag) is tuple:
                tag = nodetype[0]
                ns = nodetype[1]
            if node.tag == inkex.addNS(tag, ns) or node.tag == tag:
                constructor = SvgParser.entity_map[nodetype]
                entity = constructor()
                entity.load(node, mat)
                self.entities.append(entity)
                return entity
        return None
