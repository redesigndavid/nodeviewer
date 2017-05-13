import math

from PyQt4.QtGui import *
from PyQt4.QtCore import *

# compatibility
if not hasattr(Qt, 'MiddleButton'):
    Qt.MiddleButton = Qt.MidButton

_layers = {'edges': 2,
           'ports': 4,
           'boxes': 1,
           'nodes': 3}


class ArrowLine(QGraphicsPathItem):

    z_value = _layers.get('edges')

    def __init__(self, node_view, edge, edge_style=None, *args, **kwargs):
        super(QGraphicsPathItem, self).__init__(*args, **kwargs)
        self.setZValue(self.z_value)
        self.setAcceptsHoverEvents(True)
        self.setCacheMode(QGraphicsItem.NoCache)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self._dag_edge = edge
        self._node_view = node_view
        self._connection_data = edge._edge_data
        self._state = 'normal'
        self._points = {}

        self._dag_edge.set_ui(self)

    def style(self):
        return self._dag_edge._style

    def set_p(self, idx, p):
        self._points[idx] = QPointF(*p)

    def make_shape(self):
        p1 = self._points[0]
        bez_p1 = self._points[1]
        bez_p2 = self._points[2]
        p2 = self._points[3]

        # calculate
        self.distance = math.hypot(p1.x() - p2.x(), p1.y() - p2.y())
        quarter = (self.distance / -2)
        arrow_width = self.style().get_value('arrow_width', self._state)

        if isinstance(self._dag_edge._dst.ui(), Box):
            intersection = QPointF(*self._dag_edge._dst.ui_pos())
        else:
            stroker = QPainterPathStroker()
            stroker.setWidth(1)
            dst_shape = QPainterPath(self._dag_edge._dst.ui()._path)
            dst_shape.translate(QPointF(p1))
            dst_shape = stroker.createStroke(dst_shape)
            # self.dst_shape = QPainterPath(dst_shape)

            line_shape = QPainterPath(p1)
            line_shape.lineTo((bez_p1 * quarter) + p1)
            line_shape = stroker.createStroke(line_shape)

            intersection = line_shape.intersected(
                dst_shape).toFillPolygon().boundingRect().center()

        # self.collide = line_shape.intersected(
        #     dst_shape).toFillPolygon().boundingRect()

        s_line = QLineF(p1, (bez_p1 * quarter) + p1)
        angle = math.acos(s_line.dx() / (s_line.length() + 0.00))
        if s_line.dy() >= 0:
            angle = (math.pi * 2.0) - angle

        s_line_vec = (s_line.p2() - intersection)
        s_line_length = math.hypot(s_line_vec.x(), s_line_vec.y())
        offset = (s_line_vec / s_line_length) * 2

        arrow_p1 = intersection + QPointF(
            math.sin(angle + math.pi / 3.0) * arrow_width,
            math.cos(angle + math.pi / 3.0) * arrow_width)

        arrow_p2 = intersection + QPointF(
            math.sin(angle + math.pi - math.pi / 3.0) * arrow_width,
            math.cos(angle + math.pi - math.pi / 3.0) * arrow_width)

        self.curve_line = QPainterPath((arrow_p1 + arrow_p2) * 0.5)
        self.curve_line.cubicTo(
            (bez_p1 * quarter) + p1,
            (bez_p2 * quarter) + p2,
            p2)

        self.arrow_head = QPolygonF()
        for point in [intersection + offset, arrow_p1, arrow_p2]:
            self.arrow_head.append(point)

        stroker = QPainterPathStroker()
        stroker.setWidth(5)
        curve_stroke = QPainterPath(self.curve_line)
        curve_stroke.addPolygon(self.arrow_head)
        stroke_path = stroker.createStroke(self.curve_line)
        self.setPath(stroke_path)

    def paint(self, painter, *args, **kwargs):
        pen_width = self.style().get_value('line_width', self._state)
        color = self.style().get_value('pen_color', self._state)
        line_styles = {'solid': Qt.SolidLine,
                       'dot': Qt.DotLine,
                       'dash': Qt.DashLine}
        line_style = self.style().get_value('line_style', self._state)
        line_style = line_styles.get(line_style, Qt.SolidLine)

        pen = QPen(QColor(*color))
        pen.setWidth(pen_width)
        pen.setStyle(line_style)
        pen.setJoinStyle(Qt.MiterJoin)
        painter.setPen(pen)
        painter.drawPath(self.curve_line)
        pen.setStyle(Qt.NoPen)
        painter.setPen(pen)
        painter.setBrush(QColor(*color))
        painter.drawPolygon(self.arrow_head)

        # painter.setBrush(QColor(0,0,0,200))
        # painter.drawRect(self.collide)
        # painter.setBrush(QColor(0,255,0,200))
        # painter.drawPath(self.dst_shape)

    def hoverMoveEvent(self, event):
        self._state = 'hover'
        self.update()

    def hoverLeaveEvent(self, event):
        inherit_selection = self._node_view.inherit_selection
        if self in inherit_selection:
            self._state = 'inherit_selected'
        elif self not in self._node_view.scene.selectedItems():
            self._state = 'normal'
        else:
            self._state = 'selected'
        self.update()


class Node(QGraphicsPathItem, object):

    movable = True
    z_value = _layers.get('nodes')

    def __init__(self, node_view, node, node_style=None, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)
        self._node_view = node_view
        self._dag_node = node
        self._key = node.conn_key()
        self._state = 'normal'
        self._tip = False

        self._dag_node.set_ui(self)

        self.setAcceptsHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        if self.movable:
            self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setZValue(self.z_value)
        self.setCacheMode(QGraphicsItem.NoCache)
        self._circle = None
        self.make_shape()

    def make_shape(self):
        size = self.style().get_value('size', self._state)
        if not isinstance(size, list):
            size = [size, size]

        pen_width = self.style().get_value('line_width', self._state)
        shape = self.style().get_value('shape', self._state)

        box = QRectF(
            size[0] * -0.5,
            size[1] * -0.5,
            size[0],
            size[1])

        if shape == 'round':
            self._path = QPainterPath()
            self._path.arcMoveTo(box, 0)
            self._path.arcTo(box, 0, 360)
        elif shape == 'rect':
            self._path = QPainterPath(self.pos())
            self._path.addRect(box)

        stroker = QPainterPathStroker()
        stroker.setJoinStyle(Qt.MiterJoin)
        stroker.setWidth(pen_width)  # used as for click detection
        stroke_path = stroker.createStroke(self._path)
        stroke_path.addPolygon(self._path.toFillPolygon())
        self.setPath(stroke_path)

    def style(self):
        return self._dag_node._style

    def paint(self, painter, *args, **kwargs):
        fill_color = self.style().get_value('fill_color', self._state)
        pen_color = self.style().get_value('pen_color', self._state)
        pen_width = self.style().get_value('line_width', self._state)

        pen = QPen(QColor(*pen_color))
        pen.setWidth(pen_width)
        pen.setJoinStyle(Qt.MiterJoin)
        painter.setPen(pen)
        painter.setBrush(QColor(*fill_color))

        painter.drawPath(self._path)

    def setPos(self, x, y):
        super(Node, self).setPos(x, y)
        self._dag_node.set_pos([x, y])

    def hoverMoveEvent(self, event):
        self._state = 'hover'
        self.update()

    def hoverLeaveEvent(self, event):
        if self not in self._node_view.scene.selectedItems():
            self._state = 'normal'
        else:
            self._state = 'selected'
        self.update()

    def mousePressEvent(self, event):
        QGraphicsItem.mousePressEvent(self, event)
        if self in self._node_view.scene.selectedItems():
            self._state = 'selected'
        self.update()

    def mouseMoveEvent(self, event):
        QGraphicsItem.mouseMoveEvent(self, event)
        self.update()
        pos = [self.pos().x(), self.pos().y()]
        self._dag_node.set_pos(pos)
        nodes = [
            node._dag_node
            for node in self._node_view.scene.selectedItems()
            if hasattr(node, '_dag_node')]
        self._node_view.update_lines(nodes, fast=True)

    def mouseReleaseEvent(self, event):
        QGraphicsItem.mouseReleaseEvent(self, event)
        self.update()
        pos = [self.pos().x(), self.pos().y()]
        self._dag_node.set_pos(pos)
        nodes = self._dag_node.iter_edge_connections()
        self._node_view.update_lines(nodes, fast=False)


class Port(Node):

    movable = False
    z_value = _layers.get('ports')

    def update_pos(self):
        self.setPos(*self._dag_node.ui_pos())


class Box(Node):

    z_value = _layers.get('boxes')

    def make_shape(self):
        dim = self._dag_node._dim
        dim = [dim[0] * 0.5, dim[1] * 0.5]
        pen_width = self.style().get_value('line_width', self._state)

        box = QRectF(
            dim[0] * -0.5,
            dim[1] * -0.5,
            dim[0],
            dim[1])

        self._path = QPainterPath(self.pos())
        self._path.addRect(box)

        stroker = QPainterPathStroker()
        stroker.setJoinStyle(Qt.MiterJoin)
        stroker.setWidth(pen_width)  # used as for click detection
        stroke_path = stroker.createStroke(self._path)
        stroke_path.addPolygon(self._path.toFillPolygon())
        self.setPath(stroke_path)

    def paint(self, painter, *args, **kwargs):
        fill_color = self.style().get_value('fill_color', self._state)
        pen_color = self.style().get_value('pen_color', self._state)
        pen_width = self.style().get_value('line_width', self._state)

        pen = QPen(QColor(*pen_color))
        pen.setWidth(pen_width)
        painter.setPen(pen)
        painter.setBrush(QColor(*fill_color))

        painter.drawPath(self._path)

    def mouseMoveEvent(self, event):
        QGraphicsItem.mouseMoveEvent(self, event)
        self.update()
        pos = [self.pos().x(), self.pos().y()]
        self._dag_node.set_pos(pos)
        nodes = [
            node._dag_node
            for node in self._node_view.scene.selectedItems()
            if hasattr(node, '_dag_node')]
        ports = self._dag_node.get_ports()
        for port in ports:
            port.ui().update_pos()
        nodes.extend(ports)
        self._node_view.update_lines(nodes, fast=True)


class NodeViewer(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super(NodeViewer, self).__init__(*args, **kwargs)
        self._nodedata = None
        self.scene = QGraphicsScene(self)
        self.scene.setBackgroundBrush(QColor(100, 80, 80, 255))
        self.scene.selectionChanged.connect(self._quick_selection_changed)
        self.setScene(self.scene)
        self.setRenderHints(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setDragMode(QGraphicsView.RubberBandDrag)

        self.scene.addLine(0, 0, 0, 10)
        self.scene.addLine(0, 0, 10, 0)
        self.inherit_selection = []
        self._last_selected = []

    def _quick_selection_changed(self):
        selected_items = self.scene.selectedItems()

        for item in selected_items:
            item._state = 'consider_selection'

    def _get_selected_boxnodes(self):
        self._selected_boxnodes = [
            item for item in self.scene.selectedItems()
            if isinstance(item, (Node, Box))]
        return self._selected_boxnodes

    def _get_selected_edges(self):
        selected_nodes = self._selected_boxnodes
        selected_edges = []
        for edge in self._edges.values():

            if edge.isSelected():
                if selected_nodes:
                    edge.setSelected(False)
                else:
                    selected_edges.append(edge)
        return selected_edges

    def _selection_changed(self):
        selected_items = self.scene.selectedItems()
        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ShiftModifier:
            selected_items.extend(self._last_selected)

        selected_nodes = self._get_selected_boxnodes()
        selected_edges = self._get_selected_edges()

        iter_items = selected_nodes or selected_edges

        self.inherit_selection = []
        for item in iter_items:
            if isinstance(item, ArrowLine):
                continue
            for edge in item._dag_node.iter_edges():
                self.inherit_selection.append(edge.ui())

        for item in selected_items:
            item.setSelected(True)

        all_items = (self._nodes.values()
                     + self._edges.values()
                     + self._boxes.values())
        for item in all_items:
            if item in iter_items:
                item._state = 'selected'
            elif item in self.inherit_selection:
                item._state = 'inherit_selected'
            else:
                item._state = 'normal'

        self._last_selected = self.scene.selectedItems()

        self.update_lines()

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
        self._selection_changed()

    def wheelEvent(self, event):
        factor = math.pow(2.0, - event.delta() / 240.0)
        self.scale(factor, factor)

    def scaleView(self, scale_factor):
        factor = self.matrix().scale(
            scale_factor, scale_factor).mapRect(
                QRectF(0, 0, 1, 1)).width()

        if factor < 0.07 or factor > 100:
            return

        self.scale(scale_factor, scale_factor)

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

        # store nodes, boxes and edges qt graphic items
        self._nodes = {}
        self._boxes = {}
        self._edges = {}
        self._ports = {}
        self._node_edges = {}
        self._outgoing = {}
        self._ingoing = {}

        for nkey, data in self._graph.iter_nodes():
            node = Node(self, data)
            node.setPos(*[10 * x for x in data.get_pos()])
            self.scene.addItem(node)
            self._nodes[nkey] = node

        for bkey, data in self._graph.iter_boxes():
            box = Box(self, data)
            box.setPos(*[10 * x for x in data.get_pos()])
            self.scene.addItem(box)
            self._boxes[bkey] = box
            for dag_port in box._dag_node.get_ports():
                port = Port(self, dag_port)
                self.scene.addItem(port)
                self._ports[dag_port.conn_key()] = port
                port.setPos(*dag_port.ui_pos())

        for edge_key, edge in self._graph.iter_edges():
            gline = ArrowLine(self, edge)
            self.scene.addItem(gline)
            self._edges[edge_key] = gline

        self.update_lines()
        self.fit_in_view()

    def update_lines(self, affected_items=None, fast=False):
        items = affected_items or self.all_node_ports()

        for node in items:
            # gather node's edge's normals
            normals = node.get_edge_normals()

            # seperate the normals from each other
            if not fast:
                normals = seperate_normals(normals, repel=node.repeller())

            # assign the bezier points based on the seperated normals
            for edge_key, normal in normals.items():
                edge = self._graph.get_edge(edge_key)
                line = edge.ui()
                if edge._dst.conn_key() == node.conn_key():
                    line.set_p(0, node.ui_pos())
                    line.set_p(1, normal)
                else:
                    line.set_p(3, node.ui_pos())
                    line.set_p(2, normal)

        # update edge shapes
        for edge_key, edge in self._graph.iter_edges():
            line = edge.ui()
            line.make_shape()
            line.update()

    def all_node_ports(self):
        items = []
        for _, port in self._graph.iter_ports():
            items.append(port)
        for _, node in self._graph.iter_nodes():
            items.append(node)
        return items


def seperate_normals(normals, repel=None):
    org_norms = dict(normals)
    mult = 0.2 if not repel else 1.2
    for _ in range(4):
        for edge, normal in normals.items():
            other_norms = [
                other_norm for other_key, other_norm in normals.items()
                if other_norm != edge]
            if not other_norms:
                continue
            if repel:
                for i in range(3):
                    other_norms.append(repel)

            oxs = sum([other_norm[0] for other_norm in other_norms])
            oys = sum([other_norm[1] for other_norm in other_norms])

            temp_vec = [
                org_norms[edge][0] - ((oxs / len(other_norms)) * mult),
                org_norms[edge][1] - ((oys / len(other_norms)) * mult)]

            temp_vec_length = math.hypot(temp_vec[0], temp_vec[1])

            if not temp_vec_length:
                continue

            normals[edge] = [temp_vec[0] / temp_vec_length,
                             temp_vec[1] / temp_vec_length]

        org_norms.update(normals)
    return org_norms
