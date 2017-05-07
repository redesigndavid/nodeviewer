#!/usr/bin/env python
import subprocess


class Node():
    def __init__(self, node_key, rank_family=None, node_data=None):
        self._node_key = 'node_%s' % node_key
        self._rank_family = rank_family
        self._pos = [0, 0]
        self._node_data = node_data or {}
        self._graph = None
        self._ui = None

    def set_ui(self, item):
        self._ui = item

    def ui(self):
        return self._ui

    def set_graph(self, graph):
        self._graph = graph

    def graph(self):
        return self._graph

    def set_pos(self, pos):
        self._pos = pos

    def iter_edges(self):
        return [self.graph().get_edge(edge_key)
                for edge_key in
                self.graph()._node_edges.get(self.conn_key(), [])]

    def get_pos(self):
        return self._pos

    def conn_key(self):
        return self._node_key

    def dot_text(self):
        return "\n%s [width=1 height=1]" % self._node_key


class Edge():
    def __init__(self, s, d, w=1, edge_data=None):
        self._src = s
        self._dst = d
        self._weight = w
        self._edge_data = edge_data or {}
        self._ui = None

    def set_ui(self, item):
        self._ui = item

    def ui(self):
        return self._ui

    def key(self):
        return "%s->%s" % (self._src.conn_key(), self._dst.conn_key())

    def dot_text(self):
        return "\n%s" % ("%s -> %s [weight=%s];" % (
            self._src.conn_key(),
            self._dst.conn_key(),
            self._weight))


class Port():
    def __init__(self, box_key, d, idx):
        self._box_key = box_key
        self._d = d
        self._idx = idx

    def conn_key(self):
        return '"%s":"%s%s"' % (self._box_key, self._d, self._idx)


class Box():
    _ns_text = (
        '<TD WIDTH="{width}" HEIGHT="{height}" '
        'PORT="{d}{idx}">{d}{idx}</TD>')
    _ew_text = '<TR><TD HEIGHT="{height}" PORT="{d}{idx}">{d}{idx}</TD></TR>'
    _table_text = (
        '<TABLE BORDER="1" WIDTH="{width}" HEIGHT="{height}">'
        '<TR>'
        '<TD WIDTH="1" HEIGHT="{height}">'
        '    <TABLE BORDER="1" WIDTH="1" HEIGHT="{height}">{w}</TABLE>'
        '</TD>'
        '<TD>'
        '    <TABLE BORDER="1" WIDTH="1" HEIGHT="{height}">'
        '        <TR><TD>'
        '            <TABLE BORDER="1" WIDTH="{width}"><TR>{n}</TR></TABLE>'
        '        </TD></TR>'
        '        <TR><TD>'
        '            <TABLE BORDER="1" WIDTH="{width}"><TR>{s}</TR></TABLE>'
        '        </TD></TR>'
        '    </TABLE>'
        '</TD>'
        '<TD WIDTH="1" HEIGHT="{height}">'
        '    <TABLE  BORDER="1" WIDTH="1" HEIGHT="{height}">{e}</TABLE>'
        '</TD>'
        '</TR>'
        '</TABLE>')

    def __init__(self, n, dim, ports, rank_family=None, box_data=None):
        self._box_key = 'box_%s' % n
        self._dim = dim
        self._ports = ports
        self._rank_family = rank_family
        self._box_data = box_data or {}
        self._port_attrs = {}
        self.create_ports()
        self._pos = [0, 0]
        self._graph = None

    def set_graph(self, graph):
        self._graph = graph

    def graph(self):
        return self._graph

    def set_pos(self, pos):
        self._pos = pos

    def get_pos(self):
        return self._pos

    def create_ports(self):
        for d, n in self._ports.items():
            for idx in range(n):
                self._port_attrs[
                    (d, idx)] = Port(self._box_key, d, idx)

    def get_port(self, d, idx):
        return self._port_attrs[(d, idx)]

    def table_data(self):
        width = self._dim[0]
        height = self._dim[1]
        half_height = height / 2.0
        w_height = height / self._ports['w']
        e_height = height / self._ports['e']
        n_width = width / self._ports['n']
        s_width = width / self._ports['s']
        w = "".join(
            self._ew_text.format(
                d='w', height=w_height, idx=i)
            for i in range(self._ports['w']))
        e = "".join(
            self._ew_text.format(
                d='e', height=e_height, idx=i)
            for i in range(self._ports['e']))
        n = "".join([
            self._ns_text.format(
                width=n_width,
                height=half_height,
                idx=i, d='n')
            for i in range(self._ports['n'])])
        s = "".join([
            self._ns_text.format(
                width=s_width,
                height=half_height,
                idx=i, d='s')
            for i in range(self._ports['s'])])
        return self._table_text.format(
            width=width,
            height=height,
            half_height=half_height, w=w, e=e, n=n, s=s)

    def dot_text(self):
        text = "\n%s [shape=plaintext label=<" % (self._box_key)
        text += self.table_data()
        text += '>];\n'
        return text


class DiGraph():
    def __init__(self):
        self._edges = {}
        self._nodes = {}
        self._boxes = {}
        self._node_edges = {}
        self._node_edges = {}
        self._outgoing = {}
        self._ingoing = {}

    def add_box(self, box):
        self._boxes[box._box_key] = box

    def add_edge(self, edge):
        if edge.key() in self._edges.keys():
            return
        self._edges[edge.key()] = edge
        self._node_edges.setdefault(edge._src.conn_key(), set([])).add(edge.key())
        self._node_edges.setdefault(edge._dst.conn_key(), set([])).add(edge.key())
        self._outgoing.setdefault(edge._src, set([])).add(edge._dst)
        self._ingoing.setdefault(edge._dst, set([])).add(edge._src)

    def get_edge(self, edge_key):
        return self._edges[edge_key]

    def add_node(self, node):
        node.set_graph(self)
        self._nodes[node._node_key] = node

    def get_node(self, node_key):
        if not node_key.startswith('node_'):
            node_key = 'node_%s' % node_key
        return self._nodes[node_key]

    def iter_nodes(self):
        return [(k[len('node_'):], v)
                for k, v in self._nodes.items()]

    def iter_boxes(self):
        return [(k[len('box_'):], v)
                for k, v in self._boxes.items()]

    def iter_edges(self):
        return self._edges.items()

    def process_dot(self):
        dot_text = "digraph G {"
        for edge_key, edge in self.iter_edges():
            dot_text += edge.dot_text()

        # write in clusters
        rank_family = {}
        for node in self._nodes.values():
            rank_family.setdefault(node._rank_family or "main", []).append(node)
        for box in self._boxes.values():
            rank_family.setdefault(box._rank_family or "main", []).append(box)

        for rf, items in rank_family.items():
            dot_text += "\nsubgraph cluster_%s {rank=same; nodesep=30;" % rf

            for item in items:
                dot_text += item.dot_text()

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

        p = subprocess.Popen(
            ['dot', '-Tpng', '-o', '/var/tmp/t.png'],
            stdin=subprocess.PIPE)
        p.stdin.write(dot_text)
        p.stdin.close()

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

    for i in range(5):
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

    b = Box('sample_box', (50, 800),
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






if __name__ == '__main__':
    test()
