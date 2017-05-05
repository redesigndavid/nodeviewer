
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import math
import json
import numpy as np

import pydot

_layers = {'edges': 1,
           'nodes': 2}

class ArrowLine(QGraphicsPathItem):
    def __init__(self, node_view, connection_key, conn_data, *args, **kwargs):
        super(QGraphicsPathItem, self).__init__(*args, **kwargs)
        self._node_view = node_view
        self._key = connection_key
        self._connection_data = conn_data

        self.setZValue(_layers.get('edges'))
        self.setAcceptsHoverEvents(True)
        # self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(_layers.get('nodes'))
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        pen = QPen(QColor(*[255, 255, 255, 255]))
        pen.setWidth(10)
        self.setPen(pen)

        self._mode = 'normal'
        self.p1 = QPointF(0, 0)
        self.p2 = QPointF(0, 0)
        self.bez_p1 = QPointF(0, 0)
        self.bez_p2 = QPointF(0, 0)

    def set_p1(self, p):
        self.p1 = QPointF(*p)

    def set_bp1(self, p):
        self.bez_p1 = QPointF(*p)

    def set_p2(self, p):
        self.p2 = QPointF(*p)

    def set_bp2(self, p):
        self.bez_p2 = QPointF(*p)

    def set_points(self):
        pen_width = self._connection_data.get(
            'modes', {}).get(self._mode, {}).get('line_width')

        self.distance = math.hypot(self.p1.x() - self.p2.x(),
                                   self.p1.y() - self.p2.y())
        quarter = (self.distance / -3)

        s_line = QLineF(self.p1, (self.bez_p1 * quarter) + self.p1)
        angle = math.acos(s_line.dx() / s_line.length())
        if s_line.dy() >= 0:
            angle = (math.pi * 2.0) - angle

        s_line_vec = (s_line.p2() - s_line.p1())
        s_line_length = math.hypot(s_line_vec.x(), s_line_vec.y())
        offset = (s_line_vec / s_line_length) * 6
        arrow_size = pen_width * 2
        c_offset = (s_line_vec / s_line_length) * (6 + pen_width)
        arrowP1 = s_line.p1() + offset + QPointF(
            math.sin(angle + math.pi / 3.0) * arrow_size,
            math.cos(angle + math.pi / 3.0) * arrow_size)

        arrowP2 = s_line.p1() + offset + QPointF(
            math.sin(angle + math.pi - math.pi / 3.0) * arrow_size,
            math.cos(angle + math.pi - math.pi / 3.0) * arrow_size)

        self.curve_line = QPainterPath(self.p1 + c_offset)
        self.curve_line.cubicTo(
            (self.bez_p1 * quarter) + self.p1,
            (self.bez_p2 * quarter) + self.p2,
            self.p2)

        self.arrow_head = QPolygonF()
        for point in [s_line.p1() + offset, arrowP1, arrowP2]:
            self.arrow_head.append(point)

    def paint(self, painter, *args, **kwargs):
        color = self._connection_data.get(
            'modes', {}).get(self._mode, {}).get('pen')
        pen_width = self._connection_data.get(
            'modes', {}).get(self._mode, {}).get('line_width')
        pen = QPen(QColor(*color))
        pen.setWidth(pen_width)
        pen.setStyle(Qt.SolidLine)
        painter.setPen(pen)
        painter.drawPath(self.curve_line)
        painter.setPen(pen)
        painter.setBrush(QColor(*color))
        painter.drawPolygon(self.arrow_head)

    def shape(self):
        s = QPainterPath()
        s.addRect(self.curve_line.boundingRect())
        return s

    def boundingRect(self):
        return self.curve_line.boundingRect()




class Edge(QGraphicsLineItem):

    def __init__(self, node_view, connection_key, conn_data, *args, **kwargs):
        self._node_view = node_view
        self._key = connection_key
        self._connection_data = conn_data
        super(Edge, self).__init__(0, 0, 0, 0, *args, **kwargs)
        self.setZValue(_layers.get('edges'))
        pen = QPen(QColor(*[255, 255, 255, 255]))
        pen.setWidth(10)
        self.setPen(pen)
        self.setAcceptsHoverEvents(True)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(_layers.get('nodes'))
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self._mode = 'normal'

        self.bez_p1 = [0, 0]
        self.bez_p2 = [0, 0]

    def mousePressEvent(self, event):
        self._mode = 'selected'
        QGraphicsItem.mousePressEvent(self, event)
        self.update()

    def hoverMoveEvent(self, event):
        self._mode = 'hover'
        self.update()

    def hoverLeaveEvent(self, event):
        if self not in self._node_view.scene.selectedItems():
            self._mode = 'normal'
        else:
            self._mode = 'selected'
        self.update()

    def paint(self, painter, *args, **kwargs):
        color = self._connection_data.get(
            'modes', {}).get(self._mode, {}).get('pen')
        pen_width = self._connection_data.get(
            'modes', {}).get(self._mode, {}).get('line_width')
        pen = QPen(QColor(*color))
        pen.setWidth(pen_width)
        pen.setStyle(Qt.SolidLine)
        painter.setPen(pen)
        #path = QPainterPath(self.line().p1())
        #path.lineTo(self.line().p2())
        #painter.drawPath(path)
        line = self.line()
        quarter = (line.length() / -3)

        line = QLineF(self.line().p1(), (QPointF(*self.bez_p1) * quarter) + self.line().p1())
        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = (math.pi * 2.0) - angle

        line_vec = (line.p2() - line.p1())
        line_length = math.hypot(line_vec.x(), line_vec.y())
        offset = (line_vec / line_length) * 6
        arrow_size = pen_width * 2
        coffset = (line_vec / line_length) * (6 + pen_width)
        arrowP1 = line.p1() + offset + QPointF(
            math.sin(angle + math.pi / 3.0) * arrow_size,
            math.cos(angle + math.pi / 3.0) * arrow_size)

        arrowP2 = line.p1() + offset + QPointF(
            math.sin(angle + math.pi - math.pi / 3.0) * arrow_size,
            math.cos(angle + math.pi - math.pi / 3.0) * arrow_size)

        cline = QPainterPath(self.line().p1() + coffset)
        cline.cubicTo(
            (QPointF(*self.bez_p1) * quarter) + self.line().p1(),
            (QPointF(*self.bez_p2) * quarter) + self.line().p2(),
            self.line().p2())
        painter.drawPath(cline)

        arrow_head = QPolygonF()
        for point in [line.p1() + offset, arrowP1, arrowP2]:
            arrow_head.append(point)
        pen.setWidth(0.01)
        painter.setPen(pen)
        painter.setBrush(QColor(*color))
        painter.drawPolygon(arrow_head)


class Node(QGraphicsItem):
    def __init__(self, node_view, key, name, tooltip, modes, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)
        self._node_view = node_view
        self._key = key
        self._name = name
        self._tooltip = tooltip
        self._modes = modes
        self._mode = 'default'
        self._true_pos = None
        self._tip = False

        self.setAcceptsHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(_layers.get('nodes'))

    def paint(self, painter, *args, **kwargs):
        fill_color = self._modes.get(
            self._mode, self._modes.get('normal')).get('fill')
        pen_color = self._modes.get(
            self._mode, self._modes.get('normal')).get('pen')
        pen = QPen(QColor(*pen_color))

        pen_width = self._modes.get(
            self._mode, self._modes.get('normal')).get('line_width')
        pen.setWidth(pen_width)
        painter.setPen(pen)
        painter.setBrush(QColor(*fill_color))
        painter.drawEllipse(QRectF(-5, -5, 10, 10))

    def boundingRect(self):
        factor = 8 * self._modes.get(
            self._mode, self._modes.get('normal')).get('line_width')
        return QRectF(-5 - factor, -5 - factor, 10 + (2 * factor), 10 + (2*factor))

    def hoverMoveEvent(self, event):
        self._mode = 'hover'
        self.update()

    def hoverLeaveEvent(self, event):
        if self not in self._node_view.scene.selectedItems():
            self._mode = 'normal'
        else:
            self._mode = 'selected'
        self.update()

    def mousePressEvent(self, event):
        QGraphicsItem.mousePressEvent(self, event)
        if self in self._node_view.scene.selectedItems():
            self._mode = 'selected'
        self.update()

    def mouseMoveEvent(self, event):
        QGraphicsItem.mouseMoveEvent(self, event)
        self.update()
        pos = [self.pos().x(), self.pos().y()]
        self._node_view._nodedata['nodes'][self._key]['pos'] = pos
        self._node_view.update_lines()

    def mouseReleaseEvent(self, event):
        QGraphicsItem.mouseReleaseEvent(self, event)
        self.update()
        pos = [self.pos().x(), self.pos().y()]
        self._node_view._nodedata['nodes'][self._key]['pos'] = pos
        self._node_view.update_lines()


class NodeViewer(QGraphicsView):
    def __init__(self, node_data=None, *args, **kwargs):
        super(NodeViewer, self).__init__(*args, **kwargs)
        self._nodedata = None
        self.scene = QGraphicsScene(self)
        self.scene.setBackgroundBrush(QColor(80, 80, 80, 255))
        self.setScene(self.scene)
        self.setRenderHints(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setDragMode(QGraphicsView.RubberBandDrag)

        self.factor = 1.0
        self.set_node_data(node_data)

        self.scene.addLine(0, 0, 0, 10)
        self.scene.addLine(0, 0, 10, 0)

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            fake = QMouseEvent(
                event.type(),
                event.pos(),
                Qt.LeftButton,
                Qt.LeftButton,
                event.modifiers())
            QGraphicsView.mousePressEvent(self, fake)
        else:
            QGraphicsView.mousePressEvent(self, event)
            self.setDragMode(QGraphicsView.RubberBandDrag)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.setDragMode(QGraphicsView.RubberBandDrag)
            fake = QMouseEvent(
                event.type(),
                event.pos(),
                Qt.LeftButton,
                Qt.LeftButton,
                event.modifiers())
            QGraphicsView.mouseReleaseEvent(self, fake)
        else:
            QGraphicsView.mouseReleaseEvent(self, event)
        self.update_lines()
        selected_items = self.scene.selectedItems()
        for item in self._nodes.values() + self._edges.values():
            if item in selected_items:
                print str(item._key)
                item._mode = 'selected'
            else:
                item._mode = 'normal'

    def wheelEvent(self, event):
        self.factor = math.pow(2.0, - event.delta() / 240.0)
        self.scale(self.factor, self.factor)

    def scaleView(self, scaleFactor):
        factor = self.matrix().scale(
            scaleFactor, scaleFactor).mapRect(
                QRectF(0, 0, 1, 1)).width()

        if factor < 0.07 or factor > 100:
            return

        self.scale(scaleFactor, scaleFactor)

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
        self._node_edges = {}
        self._outgoing = {}
        self._ingoing = {}

        self._update_connection_data()

        for idx, (nkey, data) in enumerate(self._nodedata['nodes'].items()):
            node = Node(self,
                        nkey,
                        data['name'],
                        data['tooltip'],
                        data['modes'])
            pos = data.get('pos', [0, 0])
            node.setPos(pos[0], pos[1])
            self._nodes[nkey] = node

        total_connections = []
        for connection, conn_data in self._nodedata['connections'].items():
            self._node_edges.setdefault(connection[0], []).append(connection)
            self._node_edges.setdefault(connection[1], []).append(connection)
            self._outgoing.setdefault(connection[0], []).append(connection[1])
            self._ingoing.setdefault(connection[1], []).append(connection[0])
            gline = ArrowLine(self, connection, conn_data)
            self.scene.addItem(gline)
            self._edges[connection] = gline
            total_connections.extend(connection[:2])

        for key, node in self._nodes.items():
            self.scene.addItem(node)
            if total_connections.count(key) == 1:
                node._tip = True
        self.update_lines()
        self.fit_in_view()

    def _update_connection_data(self):

        for idx, (nkey, data) in enumerate(self._nodedata['nodes'].items()):
            if nkey not in self._nodes:
                continue
        self._nodedata = _get_dot_positions(**self._nodedata)

        for idx, (nkey, data) in enumerate(self._nodedata['nodes'].items()):
            if nkey not in self._nodes:
                continue
            self._nodes[nkey].setPos(*data['pos'])

    def update_lines(self, connections=None, temp=False):
        for connection in connections or self._nodedata['connections']:
            left = self._nodes[connection[0]].pos()
            right = self._nodes[connection[1]].pos()
            line = self._edges[connection]
            line.set_p1([left.x(), left.y()])
            line.set_p2([right.x(), right.y()])
        for idx, (nkey, data) in enumerate(self._nodedata['nodes'].items()):

            normals = {}

            for edge in self._node_edges[nkey]:
                if edge[0] == nkey:
                    offset = self._nodes[edge[0]].pos() - self._nodes[edge[1]].pos()
                else:
                    offset = self._nodes[edge[1]].pos() - self._nodes[edge[0]].pos()
                offset_length = math.hypot(offset.x(), offset.y())
                normal = offset / offset_length
                normals[edge] = [normal.x(), normal.y()]

            org_norms = dict(normals)
            for i in range(4):
                for edge, normal in normals.items():
                    other_norms = [
                        other_norm for other_key, other_norm in normals.items()
                        if other_norm != edge]
                    if not other_norms:
                        continue
                    oxs = sum([other_norm[0] for other_norm in other_norms])
                    oys = sum([other_norm[1] for other_norm in other_norms])
                    temp_vec = [org_norms[edge][0] - ((oxs / len(other_norms))*1.10),
                                org_norms[edge][1] - ((oys / len(other_norms))*1.10)]
                    temp_vec_length = math.hypot(temp_vec[0], temp_vec[1])
                    if not temp_vec_length:
                        continue
                    normals[edge] = [temp_vec[0] / temp_vec_length,
                                     temp_vec[1] / temp_vec_length]
            for edge, normal in normals.items():
                if edge[0] == nkey:
                    self._edges[edge].set_bp1(normal)
                else:
                    self._edges[edge].set_bp2(normal)

        for connection in connections or self._nodedata['connections']:
            left = self._nodes[connection[0]].pos()
            right = self._nodes[connection[1]].pos()
            line = self._edges[connection]
            line.set_points()
            line.update()


def _get_dot_positions(nodes=None, connections=None):
    layout_type = 'dot'
    x_factor = 1
    y_factor = 1

    if layout_type == 'dot':
        x_factor = 0.1
        y_factor = 0.1

    graph = pydot.Dot(graph_type='digraph')
    graph.set_overlap('splines')
    for conn, conn_data in connections.items():
        weight = conn_data.get('weight', 0.0)
        edge = pydot.Edge(*conn)
        edge.set_weight(weight)
        graph.add_edge(edge)

    for node_key, node_data in nodes.items():
        node = pydot.Node(node_key)
        node.set_width(3)
        node.set_height(3)
        if "pos" in node_data:
            pos = [
                node_data['pos'][0] / x_factor,
                node_data['pos'][1] / y_factor]
            node.set_pos(",".join(str(dim) for dim in pos))
        graph.add_node(node)

    json_graph = json.loads(graph.create('dot', 'json'))

    for node in json_graph['objects']:
        nodes[node['name']]['pos'] = [
            float(node['_ldraw_'][2]['pt'][0]) * x_factor,
            float(node['_ldraw_'][2]['pt'][1]) * y_factor]

    return dict(nodes=nodes, connections=connections)
