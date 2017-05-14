#!/usr/bin/env python
import uuid
import subprocess
import math
from node_viewer import style


def memoize(function):
    memo = {}

    def wrapper(*args):
        if args in memo:
            return memo[args]
        else:
            rv = function(*args)
            memo[args] = rv
            return rv

    return wrapper

_keys = []


def unique_key():
    import random
    global _keys
    key = None
    while not key or key in _keys:
        key = ''
        for i in range(16):
            key += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    _keys.append(key)
    return key


class Node(object):
    def __init__(self, node_label, rank_family=None, node_data=None, uid=None):
        self._label = node_label
        self._id = 'node_%s' % (uid or unique_key())
        self._rank_family = rank_family
        self._pos = [0, 0]
        self._node_data = node_data or {}
        self._graph = None
        self._ui = None
        self._style = style.NodeStyle()

    def label(self):
        return self._label

    def style(self):
        return self._style

    def repeller(self):
        return None

    def set_ui(self, item):
        self._ui = item

    def ui(self):
        return self._ui

    def ui_pos(self):
        pos = self.ui().pos()
        return [pos.x(), pos.y()]

    def set_graph(self, graph):
        self._graph = graph

    def graph(self):
        return self._graph

    def set_pos(self, pos):
        self._pos = pos

    @memoize
    def iter_edges(self):
        return [self.graph().get_edge(edge_key)
                for edge_key in
                self.graph()._node_edges.get(self.key(), [])]

    def get_edge_normals(self):
        # gather node's edge's normals
        normals = {}
        for edge in self.iter_edges():
            is_forwards = (edge._src.key() == self.key())
            offset = [
                edge._src.ui_pos()[0] - edge._dst.ui_pos()[0],
                edge._src.ui_pos()[1] - edge._dst.ui_pos()[1]]
            if not is_forwards:
                offset = [dim * -1 for dim in offset]
            offset_length = math.hypot(offset[0], offset[1])
            normal = [dim / offset_length for dim in offset]
            normals[edge.key()] = normal
        return normals

    @memoize
    def iter_edge_connections(self):
        edge_connections = set([])
        for edge in self.iter_edges():
            edge_connections.add(edge._src)
            edge_connections.add(edge._dst)
        return list(edge_connections)

    @memoize
    def dot_text(self):
        return "\n%s [width=1 height=1]" % self._id

    def get_pos(self):
        return self._pos

    def key(self):
        return self._id


class Edge():
    def __init__(self, s, d, w=1, edge_data=None):
        self._src = s
        self._dst = d
        self._weight = w
        self._edge_data = edge_data or {}
        self._ui = None
        self._style = style.EdgeStyle()

    def style(self):
        return self._style

    def set_ui(self, item):
        self._ui = item

    def ui(self):
        return self._ui

    @memoize
    def key(self):
        return "%s->%s" % (self._src.key(), self._dst.key())

    @memoize
    def dot_text(self):
        return "\n%s" % ("%s -> %s [weight=%s];" % (
            self._src.key(),
            self._dst.key(),
            self._weight))


class Port():

    def __init__(self, box, d, idx):
        self._box = box
        self._box_key = box.key()
        self._d = d
        self._idx = idx
        self._ui = None
        self._style = style.NodeStyle()
        self._repeller = {
            'n': [0, -1],
            's': [0, 1],
            'e': [1, 0],
            'w': [-1, 0]}[self._d]
        self._label = 'port'

    def label(self):
        return self._label

    def set_label(self, label_text):
        self._label = label_text

    def set_pos(self, *args, **kwargs):
        pass

    @memoize
    def iter_edge_connections(self):
        edge_connections = set([])
        for edge in self.iter_edges():
            edge_connections.add(edge._src)
            edge_connections.add(edge._dst)
        return list(edge_connections)

    def calc_pos(self):
        '''calculate port position based on box dimensions'''
        dim = [d * -0.5 for d in self._box._dim]
        mult = self._box._ports[self._d]
        idx = (self._idx - (mult * 0.5)) + 0.5
        offset = {
            'n': [
                (dim[0] * 0.9 / mult) * idx,
                dim[1] * 0.5],
            's': [
                (dim[0] * 0.9 / mult) * idx,
                dim[1] * -0.5],
            'e': [
                dim[0] * -0.5,
                (dim[1] * 0.9 / mult) * idx],
            'w': [
                dim[0] * 0.5,
                (dim[1] * 0.9 / mult) * idx]}[self._d]

        pos = self._box.ui_pos()
        self._pos = [pos[0] + offset[0], pos[1] + offset[1]]

    def repeller(self):
        return self._repeller

    def ui_pos(self):
        return self._pos

    @memoize
    def key(self):
        return '"%s":"%s%s"' % (self._box_key, self._d, self._idx)

    def set_ui(self, item):
        self._ui = item

    def ui(self):
        return self._ui

    @memoize
    def iter_edges(self):
        return [self._box.graph().get_edge(edge_key)
                for edge_key in
                self._box.graph()._node_edges.get(
                    self.key(), [])]

    def get_edge_normals(self):
        # gather node's edge's normals
        normals = {}
        for edge in self.iter_edges():
            is_forwards = (edge._src.key() == self.key())
            offset = [
                edge._src.ui_pos()[0] - edge._dst.ui_pos()[0],
                edge._src.ui_pos()[1] - edge._dst.ui_pos()[1]]
            if not is_forwards:
                offset = [dim * -1 for dim in offset]
            offset_length = math.hypot(offset[0], offset[1])
            normal = [dim / offset_length for dim in offset]
            normals[edge.key()] = normal
        return normals


class Box():
    _ns_text = (
        '<TD WIDTH="{width}" HEIGHT="{height}" '
        'PORT="{d}{idx}">{d}{idx}</TD>')
    _ew_text = '<TR><TD HEIGHT="{height}" PORT="{d}{idx}">{d}{idx}</TD></TR>'
    _table_text = (
        '<TABLE BORDER="1" WIDTH="{width}" HEIGHT="{height}">'
        '<TR>'
        '<TD WIDTH="1" HEIGHT="{height}">'
        '    <TABLE BORDER="0" WIDTH="1" HEIGHT="{height}">{w}</TABLE>'
        '</TD>'
        '<TD>'
        '    <TABLE BORDER="0" WIDTH="1" HEIGHT="{height}">'
        '        <TR><TD>'
        '            <TABLE BORDER="0" WIDTH="{width}"><TR>{n}</TR></TABLE>'
        '        </TD></TR>'
        '        <TR><TD>'
        '            <TABLE BORDER="0" WIDTH="{width}"><TR>{s}</TR></TABLE>'
        '        </TD></TR>'
        '    </TABLE>'
        '</TD>'
        '<TD WIDTH="1" HEIGHT="{height}">'
        '    <TABLE  BORDER="0" WIDTH="1" HEIGHT="{height}">{e}</TABLE>'
        '</TD>'
        '</TR>'
        '</TABLE>')

    def __init__(self, n, dim, ports, rank_family=None, box_data=None, uid=None):
        self._id = 'box_%s' % (uid or unique_key())
        self._ports = ports
        self._rank_family = rank_family
        self._box_data = box_data or {}
        self._node_data = box_data  # temp
        self._port_attrs = {}
        self._pos = [0, 0]
        self._graph = None
        self._ui = None
        self._dim = dim
        self.set_dim(dim)
        self.create_ports()
        self._style = style.NodeStyle()
        self._label = 'box'

    def label(self):
        return self._label

    def get_edge_normals(self):
        return {}

    def style(self):
        return self._style

    def set_dim(self, dim):
        self._dim = dim
        for port in self._port_attrs.values():
            # update ports
            port.calc_pos()

    def get_dim(self):
        return self._dim

    def set_ui(self, item):
        for port in self._port_attrs.values():
            # update ports
            port.calc_pos()
        self._ui = item

    def iter_edge_connections(self):
        edge_connections = set([])
        for port in self._port_attrs.values():
            for edge in port.iter_edges():
                edge_connections.add(edge._src)
                edge_connections.add(edge._dst)

        return list(edge_connections)

    def iter_edges(self):
        edges = []
        for port in self._port_attrs.values():
            edges.extend(port.iter_edges())
        return edges

    def ui(self):
        return self._ui

    def ui_pos(self):
        return self._pos

    def set_graph(self, graph):
        self._graph = graph

    def graph(self):
        return self._graph

    def set_pos(self, pos):
        self._pos = pos
        for port in self._port_attrs.values():
            # update ports
            port.calc_pos()

    def get_pos(self):
        return self._pos

    def key(self):
        return self._id

    def create_ports(self):
        for d, n in self._ports.items():
            for idx in range(n):
                self._port_attrs[
                    (d, idx)] = Port(self, d, idx)

    def get_port(self, d, idx):
        return self._port_attrs[(d, idx)]

    def get_ports(self):
        return self._port_attrs.values()

    def table_data(self):
        width = self._dim[0] * 1.4
        height = self._dim[1] * 1.4
        half_height = height / 2.0

        w = (self._ports['w'] and "".join(
            self._ew_text.format(
                d='w',
                height=height / self._ports['w'],
                idx=i)
            for i in range(self._ports['w']))
            or "<TD>NULL</TD>")
        e = (self._ports['e'] and "".join(
            self._ew_text.format(
                d='e',
                height=height / self._ports['e'],
                idx=i)
            for i in range(self._ports['e']))
            or "<TD>NULL</TD>")
        n = (self._ports['n'] and "".join([
            self._ns_text.format(
                width=width / self._ports['n'],
                height=half_height,
                idx=i, d='n')
            for i in range(self._ports['n'])])
            or "<TD>NULL</TD>")
        s = (self._ports['s'] and " ".join([
            self._ns_text.format(
                width=width / self._ports['s'],
                height=half_height,
                idx=i, d='s')
            for i in range(self._ports['s'])])
            or "<TD>NULL</TD>")

        return self._table_text.format(
            width=width,
            height=height,
            half_height=half_height, w=w, e=e, n=n, s=s)

    def dot_text(self):
        text = "\n%s [shape=plaintext label=<" % (self.key())
        text += self.table_data()
        text += '>];\n'
        return text


class DiGraph():
    def __init__(self):
        self._edges = {}
        self._nodes = {}
        self._boxes = {}
        self._ports = {}
        self._node_edges = {}
        self._node_edges = {}
        self._outgoing = {}
        self._ingoing = {}

    def add_box(self, box):
        box.set_graph(self)
        self._boxes[box.key()] = box

        for port in box.get_ports():
            self._ports[port.key()] = port

    def add_edge(self, edge):
        if edge.key() in self._edges.keys():
            return
        self._edges[edge.key()] = edge
        self._node_edges.setdefault(edge._src.key(), set([])).add(edge.key())
        self._node_edges.setdefault(edge._dst.key(), set([])).add(edge.key())
        self._outgoing.setdefault(edge._src, set([])).add(edge._dst)
        self._ingoing.setdefault(edge._dst, set([])).add(edge._src)

    def get_edge(self, edge_key):
        return self._edges[edge_key]

    def add_node(self, node):
        node.set_graph(self)
        self._nodes[node._id] = node

    def get_node(self, node_key):
        if not node_key.startswith('node_'):
            node_key = 'node_%s' % node_key
        return self._nodes[node_key]

    def iter_nodes(self):
        return [(k[len('node_'):], v)
                for k, v in self._nodes.items()]

    def iter_ports(self):
        return [(k[len('node_'):], v)
                for k, v in self._ports.items()]

    def iter_boxes(self):
        return [(k[len('box_'):], v)
                for k, v in self._boxes.items()]

    def iter_edges(self):
        return self._edges.items()

    def all_routes(self):
        all_items = (
            self._nodes.values()
            + self._boxes.values()
            + self._ports.values())

        connected_nodes = [
            item for item in all_items if item.iter_edges()]

        starts = [
            item for item in connected_nodes
            if not self._ingoing.get(item)]

        paths = []

        def dfs(item, history=None, visited=None):
            if not history:
                history = [item]
            else:
                history = history[:]
                history.append(item)

            if not visited:
                visited = [item]
            else:
                visited = visited[:]
                visited.append(item)

            outgoings = [
                og for og in list(
                    self._outgoing.get(item, []))
                if og not in visited]

            if not outgoings:
                paths.append(history[:])
            else:
                for outgoing in outgoings:
                    dfs(outgoing, history, visited)

        for item in starts:
            dfs(item)

        return paths

    def find_matching_bookends(self):
        same_source_and_end = []

        # look for routes with matching start and ends
        same_start_ends = {}
        for route in self.all_routes():
            if len(route) < 2:
                continue
            same_start_ends.setdefault(
                (route[0], route[-1], len(route)), []).append(route)

        # for every group of matching start and end
        # look for contiguous matching
        for routes in same_start_ends.values():
            if len(routes) < 2:
                continue

            matching = [
                len(set([route[idx] for route in routes])) != 1
                for idx in range(len(routes[0]))]

            # find contiguous groups
            prev = None
            group = []
            groups = []
            for idx in range(len(matching)):
                if matching[idx]:
                    group.append(idx)
                elif prev and matching[idx]:
                    group.append(idx)
                elif prev and not matching[idx]:
                    groups.append(group)
                    group = []
                prev = matching[idx]
            for group in groups:
                items = []
                for idx in group:
                    items.extend([route[idx] for route in routes])
                same_source_and_end.append(items)

        return same_source_and_end

    def process_dot(self, autosubgraph=True):

        dot_text = "digraph G {"
        dot_text += "\nnode[fontsize=1]\n"

        for edge_key, edge in self.iter_edges():
            dot_text += edge.dot_text()

        # write in clusters
        rank_family = {}
        if autosubgraph:
            node_groups = {}
            group_nodes = dict(enumerate(self.find_matching_bookends()))

            for idx, node_group in group_nodes.items():
                for node in node_group:
                    node_groups[node] = idx
            for node in self._nodes.values():
                idx = node_groups.get(node, 'main')
                rank_family.setdefault(
                    'group%s' % idx, []).append(node)
            for box in self._boxes.values():
                idx = node_groups.get(box, 'main')
                rank_family.setdefault(
                    'group%s' % idx, []).append(box)

        else:
            for node in self._nodes.values():
                rank_family.setdefault(
                    node._rank_family or "main", []).append(node)
            for box in self._boxes.values():
                rank_family.setdefault(
                    box._rank_family or "main", []).append(box)

        for rf, items in rank_family.items():
            if rf != 'groupmain':
                dot_text += "\nsubgraph cluster_%s {rank=same; nodesep=30;" % rf

            for item in items:
                dot_text += item.dot_text()
            if rf != 'groupmain':
                dot_text += "}\n"

        dot_text += "}\n"

        p = subprocess.Popen(
            ['dot'],
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE)
        p.stdin.write(dot_text)
        p.stdin.close()
        dot_text = p.stdout.read()

        p = subprocess.Popen(
            ['unflatten', '-l', '300', '-f', '-c', '300'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
        p.stdin.write(dot_text)
        p.stdin.close()
        dot_text = p.stdout.read()

        p = subprocess.Popen(
            ['dot', '-Tplain-ext'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
        p.stdin.write(dot_text)
        p.stdin.close()
        plain_text = p.stdout.read()

        #p = subprocess.Popen(
        #    ['dot', '-Tpng', '-o', '/var/tmp/t.png'],
        #    stdin=subprocess.PIPE)
        #p.stdin.write(dot_text)
        #p.stdin.close()

        for line in dot_text.splitlines():
            if line.count('cluster'):
                print line
        for line in plain_text.splitlines():
            line = line.strip()
            if not line.startswith('node'):
                continue
            _, item_key, x, y = line.split()[:4]
            item_key = item_key.strip('"')
            if item_key in self._nodes:
                self._nodes[item_key].set_pos((float(x) * 3, float(y) * -3))
            else:
                self._boxes[item_key].set_pos((float(x) * 3, float(y) * -3))


def test():
    digraph = DiGraph()
    n = []

    clus = ['foo', 'bar']

    import random

    def random_key():
        nm = ""
        for _ in range(5):
            nm += random.choice('abcdefghijklmnopqrstuvwxyz')
        return nm

    for i in range(30):
        node_mode = {'normal': {}, 'selected': {}, 'hover': {}}
        color = [random.random() * 55, random.random() * 255, random.random() * 50, 255]
        node_mode['normal']['fill'] = color
        node_mode['normal']['pen'] = color
        node_mode['selected']['pen'] = [155, 155, 155, 255]
        node_mode['selected']['fill'] = [155, 155, 155, 255]
        node_mode['hover']['pen'] = [255, 255, 255, 255]
        node_mode['hover']['fill'] = [255, 255, 255, 255]
        k = Node(random_key(), random.choice(clus), node_data={'modes': node_mode})
        digraph.add_node(k)
        n.append(k)

    for node in n:
        for i in range(random.choice(range(2)) + 1):
            color = node._node_data['modes']['normal']['fill']
            edge_mode = {'normal': {}, 'hover': {}, 'selected': {}}
            edge_mode['normal']['pen'] = color
            edge_mode['hover']['pen'] = [255, 255, 255, 255]
            edge_mode['selected']['pen'] = [155, 155, 155, 255]
            conn = random.choice(n)
            e = Edge(node, conn, edge_data={'modes': edge_mode})
            digraph.add_edge(e)

    b = Box('sample_box', (150, 80),
            {'n': 3, 's': 2, 'w': 4, 'e': 5},
            random.choice(clus),
            box_data={'modes': node_mode})
    digraph.add_box(b)

    e = Edge(b.get_port('n', 1), random.choice(n))
    digraph.add_edge(e)

    for i in range(2):
        e = Edge(b.get_port('e', 0), random.choice(n))
        digraph.add_edge(e)

    digraph.process_dot()

    for edge_key, edge in digraph.iter_edges():
        print edge.key()

    for node_key, node_data in digraph.iter_nodes():
        print node_key, node_data.get_pos()
    for node_key, node_data in digraph.iter_boxes():
        print node_key, node_data.get_pos()
    print '--'
    for node_key, node_data in digraph.iter_nodes():
        print '-'
        print node_key
        for edge in node_data.iter_edges():
            print edge.key()
    print '---'

    same_source_and_end = digraph.find_matching_bookends()

    for group in same_source_and_end:
        print [nod.key() for nod in group]



if __name__ == '__main__':
    test()
