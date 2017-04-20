
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import random
import numpy as np


class Edge(QGraphicsLineItem):
    def __init__(self, *args, **kwargs):
        super(Edge, self).__init__(*args, **kwargs)

    def paint(self, painter, *args, **kwargs):
        super(Edge, self).paint(painter, *args, **kwargs)
        # middle = (self.line().p2() + self.line().p1()) / 2.0
        # painter.drawText(middle, "%.02f" % self.line().length())


class Node(QGraphicsItem):
    def __init__(self, node_view, key, name, tooltip, colors, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)
        self._node_view = node_view
        self._key = key
        self._name = name
        self._tooltip = tooltip
        self._colors = colors
        self._mode = 'default'
        self._true_pos = None
        self._tip = False

    def paint(self, painter, *args, **kwargs):
        color = self._colors.get(self._mode)
        line_color = self._colors.get('line')
        painter.setPen(QColor(*line_color))
        painter.setBrush(QColor(*color))
        painter.drawEllipse(QRectF(-5, -5, 10, 10))

    def boundingRect(self):
        return QRectF(-5, -5, 10, 10)


class NodeViewer(QGraphicsView):
    def __init__(self, node_data=None, *args, **kwargs):
        super(NodeViewer, self).__init__(*args, **kwargs)
        self._nodedata = None
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHints(QPainter.Antialiasing)

        self.set_node_data(node_data)

        self.scene.addLine(0, 0, 0, 10)
        self.scene.addLine(0, 0, 10, 0)

        # set time line animator
        self._timeline = QTimeLine(1000)
        self._timeline.setFrameRange(0, 99)
        self._timeline.setLoopCount(0)
        self._timeline.frameChanged.connect(self.frame_update)
        self._timeline.start()

        self._iters = 10000

    def frame_update(self, frame):

        self._iters -= 20
        self._iters = max(10, self._iters)

        mult = float(self._iters) / 10000.0

        _spring_damp = 0.055 * mult
        _spring_length = 35
        _repel_strength = 22.8 * mult

        nodes_num = len(self._nodes)
        sorted_keys = sorted(self._nodes.keys())
        n = np.zeros((nodes_num, 2))
        for idx, sorted_key in enumerate(sorted_keys):
            try:
                node = self._nodes[sorted_key]
                n[idx] = np.array((node.pos().x(), node.pos().y()))
            except KeyError:
                line = self._edges[sorted_key]
                p = (line.line().p2() + line.line().p1()) / 2.0
                n[idx] = np.array((p.x(), p.y()))

        c = np.zeros((nodes_num, nodes_num))
        c.fill(np.nan)
        for connection in self._nodedata['connections']:
            idx = sorted_keys.index(connection[0])
            idy = sorted_keys.index(connection[1])
            c[idx, idy] = 1.0
        c[np.isnan(c)] = 0.0

        siblings = []
        for idx in range(c.shape[0]):
            s = c[np.where(c[idx] == 1)].sum(axis=0)
            s[idx] = 0
            siblings.append(s)

        # we want random rather than zeros
        delta = np.random.random((
            n.shape[0], n.shape[0], n.shape[1]))

        for i in range(3):

            for i in xrange(n.shape[1]):
                # matrix of difference between points
                delta[:, :, i] = n[:, i, None] - n[:, i]

            # distance betwen points
            distance = np.sqrt((delta**2).sum(axis=-1))
            distance = np.where(distance < 0.0001, 0.0001, distance)

            # repel displacement
            repl_normal_direction = np.transpose(delta) / distance
            repl_direction = (
                    repl_normal_direction
                    * _repel_strength
                    / (distance**2))
            repel_disp = np.transpose(repl_direction).sum(axis=1)

            # calculate attraction
            delta[np.where(c == 0.0)] = 0
            length = np.sqrt((delta**2).sum(axis=-1))
            length = np.where(length < 0.0001, 0.0001, length)
            stretch = np.transpose(length) - _spring_length
            attract = (np.transpose(delta * -1) / np.transpose(length)
                       * stretch * _spring_damp).transpose().sum(axis=1)

            n = attract + repel_disp + n

        for idx, sorted_key in enumerate(sorted_keys):
            try:
                node = self._nodes[sorted_key]
                d = n[idx]
                p = QPointF(d[0], d[1])
                node.setPos(p)
            except:
                pass

        # update lines
        for connection in self._nodedata['connections']:
            left = self._nodes[connection[0]].pos()
            right = self._nodes[connection[1]].pos()
            line = self._edges[connection]
            line.setLine(QLineF(left.x(), left.y(),
                                right.x(), right.y()))

    def fit_in_view(self):
        xs = [nod.pos().x() for nod in self._nodes.values()]
        ys = [nod.pos().y() for nod in self._nodes.values()]
        minx = min(xs)
        miny = min(ys)
        maxx = max(xs)
        maxy = max(ys)
        self.fitInView(
                minx, miny, maxx - minx, maxy - miny,
                Qt.KeepAspectRatio)

    def set_node_data(self, node_data):

        self._nodedata = node_data or {}

        # store nodes and edges qt graphic items
        self._nodes = {}
        self._edges = {}

        for idx, (nkey, data) in enumerate(self._nodedata['nodes'].items()):
            node = Node(self,
                        nkey,
                        data['name'],
                        data['tooltip'],
                        data['colors'])
            node.setPos(random.random() * 200, random.random() * 200)
            self._nodes[nkey] = node

        total_connections = []
        for connection in self._nodedata['connections']:
            gline = Edge(0, 0, 0, 0)
            self.scene.addItem(gline)
            self._edges[connection] = gline

            total_connections.extend(connection[:2])

        for key, node in self._nodes.items():
            self.scene.addItem(node)

            if total_connections.count(key) == 1:
                node._tip = True


def _rescale_layout(pos, scale=1):
    # rescale to (0,pscale) in all axes

    # shift origin to (0,0)
    lim = 0  # max coordinate for all axes
    for i in xrange(pos.shape[1]):
        pos[:, i] -= pos[:, i].min()
        lim = max(pos[:, i].max(), lim)
    # rescale to (0,scale) in all directions, preserves aspect
    for i in xrange(pos.shape[1]):
        pos[:, i] *= scale / lim
    return pos
