
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import math
import dag

# compatibility
if not hasattr(Qt, 'MiddleButton'):
    Qt.MiddleButton = Qt.MidButton

_layers = {'edges': 3,
           'nodes': 2}


class ArrowLine(QGraphicsPathItem):
    def __init__(self, node_view, edge, *args, **kwargs):
        super(QGraphicsPathItem, self).__init__(*args, **kwargs)
        self._dag_edge = edge
        self._node_view = node_view
        self._connection_data = edge._edge_data
        edge.set_ui(self)

        self.setZValue(_layers.get('edges'))
        self.setAcceptsHoverEvents(True)
        self.setCacheMode(QGraphicsItem.NoCache)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self._mode = 'normal'

        self._points = {}

    def set_p(self, idx, p):
        self._points[idx] = QPointF(*p)

    def make_shape(self):
        if len(self._points) < 4:
            return
        p1 = self._points[0]
        bez_p1 = self._points[1]
        bez_p2 = self._points[2]
        p2 = self._points[3]

        pen_width = self._connection_data.get(
            'modes', {}).get(self._mode, {}).get('line_width', 1.5)

        self.distance = math.hypot(p1.x() - p2.x(),
                                   p1.y() - p2.y())
        quarter = (self.distance / -3)

        s_line = QLineF(p1, (bez_p1 * quarter) + p1)
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

        self.curve_line = QPainterPath(p1 + c_offset)
        self.curve_line.cubicTo(
            (bez_p1 * quarter) + p1,
            (bez_p2 * quarter) + p2,
            p2)

        self.arrow_head = QPolygonF()
        for point in [s_line.p1() + offset, arrowP1, arrowP2]:
            self.arrow_head.append(point)

        stroker = QPainterPathStroker()
        stroker.setWidth(5)
        curve_stroke = QPainterPath(self.curve_line)
        curve_stroke.addPolygon(self.arrow_head)
        stroke_path = stroker.createStroke(self.curve_line)
        self.setPath(stroke_path)

    def paint(self, painter, *args, **kwargs):
        if len(self._points) < 4:
            return
        color = self._connection_data.get(
            'modes', {}).get(self._mode, {}).get(
                    'pen', [255, 255, 255, 255])
        pen_width = self._connection_data.get(
            'modes', {}).get(self._mode, {}).get('line_width', 1.5)
        pen = QPen(QColor(*color))
        pen.setWidth(pen_width)
        pen.setStyle(Qt.SolidLine)
        pen.setJoinStyle(Qt.MiterJoin)
        painter.setPen(pen)
        painter.drawPath(self.curve_line)
        pen.setStyle(Qt.NoPen)
        painter.setPen(pen)
        painter.setBrush(QColor(*color))
        painter.drawPolygon(self.arrow_head)

    def hoverMoveEvent(self, event):
        self._mode = 'hover'
        self.update()

    def hoverLeaveEvent(self, event):
        if self not in self._node_view.scene.selectedItems():
            self._mode = 'normal'
        else:
            self._mode = 'selected'
        self.update()


class Node(QGraphicsItem):
    def __init__(self, node_view, node, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)
        self._node_view = node_view
        self._dag_node = node
        self._dag_node.set_ui(self)
        self._key = node.conn_key()
        self._modes = node._node_data.get('modes')
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
        factor = 0.5 * self._modes.get(
            self._mode, self._modes.get('normal')).get('line_width')
        return QRectF(
                -5 - factor,
                -5 - factor,
                10 + (2 * factor),
                10 + (2 * factor))

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
        self._dag_node.set_pos(pos)
        self._node_view.update_lines()

    def mouseReleaseEvent(self, event):
        QGraphicsItem.mouseReleaseEvent(self, event)
        self.update()
        pos = [self.pos().x(), self.pos().y()]
        self._dag_node.set_pos(pos)
        self._node_view.update_lines()


class Box(Node):
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
        dim = self._dag_node._dim
        dim = [dim[0] * 0.5, dim[1] * 0.5]
        painter.drawRect(QRectF(
            -0.5 * dim[0], -0.5 * dim[1],
            dim[0], dim[1]))

    def boundingRect(self):
        dim = self._dag_node._dim
        dim = [dim[0] * 0.5, dim[1] * 0.5]
        return QRectF(
            -0.5 * dim[0], -0.5 * dim[1],
            dim[0], dim[1])


class NodeViewer(QGraphicsView):
    def __init__(self, *args, **kwargs):
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
        self.setDragMode(QGraphicsView.RubberBandDrag)
        if event.button() == Qt.MiddleButton:
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

    def set_node_data(self, graph):
        self._graph = graph

        self._nodedata = {}

        # store nodes and edges qt graphic items
        self._nodes = {}
        self._edges = {}
        self._node_edges = {}
        self._outgoing = {}
        self._ingoing = {}

        for nkey, data in self._graph.iter_nodes():
            node = Node(self, data)
            node.setPos(*[10 * x for x in data.get_pos()])
            self.scene.addItem(node)
            self._nodes[nkey] = node

        for nkey, data in self._graph.iter_boxes():
            node = Box(self, data)
            node.setPos(*[10 * x for x in data.get_pos()])
            self.scene.addItem(node)
            self._nodes[nkey] = node

        for edge_key, edge in self._graph.iter_edges():
            gline = ArrowLine(self, edge)
            self.scene.addItem(gline)

        """
        for connection, conn_data in self._nodedata['connections'].items():

            self._node_edges.setdefault(connection[0], []).append(connection)
            self._node_edges.setdefault(connection[1], []).append(connection)
            self._outgoing.setdefault(connection[0], []).append(connection[1])
            self._ingoing.setdefault(connection[1], []).append(connection[0])

            gline = ArrowLine(self, connection, conn_data)
            self.scene.addItem(gline)
            self._edges[connection] = gline
        """

        # self.update_nodes()
        self.update_lines()
        # self.fit_in_view()

    def update_nodes(self):

        # calculate nodes from graphviz
        self._nodedata = _get_dot_positions(**self._nodedata)

        for nkey, data in self._nodedata['nodes'].items():
            if nkey not in self._nodes:
                # bad node
                continue
            self._nodes[nkey].setPos(*data['pos'])

    def update_lines(self, connections=None, temp=False):
        items = []
        for _, port in self._graph.iter_ports():
            items.append(port)
        for _, node in self._graph.iter_nodes():
            items.append(node)

        for node in items:

            # gather node's edge's normals
            normals = {}

            for edge in node.iter_edges():
                is_forwards = (edge._src.conn_key() == node.conn_key())
                offset = (edge._src.ui_pos() - edge._dst.ui_pos())
                if not is_forwards:
                    offset *= -1
                offset_length = math.hypot(offset.x(), offset.y())
                normal = offset / offset_length
                normals[edge.key()] = [normal.x(), normal.y()]

            # seperate the normals from each other
            normals = seperate_normals(normals, repel=node.repeller())

            # assign the bezier points based on the seperated normals
            for edge_key, normal in normals.items():
                edge = self._graph.get_edge(edge_key)
                line = edge.ui()
                if edge._dst.conn_key() == node.conn_key():
                    line.set_p(0, [node.ui_pos().x(), node.ui_pos().y()])
                    line.set_p(1, normal)
                else:
                    line.set_p(3, [node.ui_pos().x(), node.ui_pos().y()])
                    line.set_p(2, normal)

        # update edge shapes
        for edge_key, edge in self._graph.iter_edges():
            line = edge.ui()
            try:
                line.make_shape()
                line.update()
            except:
                print 'bad'


def seperate_normals(normals, repel=None):
    org_norms = dict(normals)

    for _ in range(4):
        for edge, normal in normals.items():
            other_norms = [
                other_norm for other_key, other_norm in normals.items()
                if other_norm != edge]
            if not other_norms:
                continue
            if repel:
                for i in range(10):
                    other_norms.append(repel)
            oxs = sum([other_norm[0] for other_norm in other_norms])
            oys = sum([other_norm[1] for other_norm in other_norms])
            temp_vec = [org_norms[edge][0] - ((oxs / len(other_norms))*1.10),
                        org_norms[edge][1] - ((oys / len(other_norms))*1.10)]
            temp_vec_length = math.hypot(temp_vec[0], temp_vec[1])
            if not temp_vec_length:
                continue
            normals[edge] = [temp_vec[0] / temp_vec_length,
                             temp_vec[1] / temp_vec_length]
        org_norms.update(normals)
    return org_norms


def _get_dot_positions(nodes=None, connections=None):
    layout_type = 'dot'
    x_factor = 1
    y_factor = 1

    if layout_type == 'dot':
        x_factor = 10
        y_factor = 10

    graph = dag.DiGraph()

    for node_key, node_data in nodes.items():
        node = dag.Node(node_key)
        graph.add_node(node)

    for conn, conn_data in connections.items():
        edge = dag.Edge(
            graph.get_node(conn[0]),
            graph.get_node(conn[1]))
        graph.add_edge(edge)

    graph.process_dot()

    for node_key, node_data in graph.iter_nodes():
        node_data = node_data.get_pos()
        nodes[node_key]['pos'] = [float(node_data[0]) * x_factor,
                                  float(node_data[1]) * y_factor]

    return dict(nodes=nodes, connections=connections)
