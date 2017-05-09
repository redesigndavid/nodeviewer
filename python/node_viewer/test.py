import sys
from PyQt4.QtGui import QApplication
from node_viewer import NodeViewer
import random


_default_node_modes = {
    'normal': {
        'fill': (0, 250, 0, 255),
        'pen': (0, 250, 0, 255),
        'line_width': 1.5,
    },
    'selected': {
        'fill': (255, 225, 0, 255),
        'pen': (200, 30, 50, 255),
        'line_width': 1.5,

    },
    'click': {
        'fill': (155, 200, 0, 255),
        'pen': (200, 200, 220, 255),
        'line_width': 1.5,
    },
    'hover': {
        'fill': (155, 200, 0, 255),
        'pen': (200, 80, 220, 255),
        'line_width': 1.5,
    },
}

_default_line_modes = {
    'normal': {
        'pen': (0, 255, 0, 255),
        'line_width': 1.5
    },
    'selected': {
        'pen': (120, 255, 255, 255),
        'line_width': 1.5
    },
    'hover': {
        'pen': (255, 255, 20, 255),
        'line_width': 1.5
    },
}


def rand_key():
    letters = (
        'ABCDEFGHIJKLMNOPQRSTUV'
        'abcdefghijklmnopqrstuv'
        '01234567890')
    rtn = ''
    for i in range(4):
        rtn += random.choice(letters)
    return rtn


_test_data = {
    'nodes': {
        'defg': {'name': 'Asterisk *',
              'modes': _default_node_modes,
              'tooltip': '*'},
        'bcde': {'name': 'Bang !',
              'modes': _default_node_modes,
              'tooltip': '!'},
        'abcd': {'name': 'Comma ,',
              'modes': _default_node_modes,
              'tooltip': ','},
    },
    'connections': {
        ('defg', 'bcde'): {'modes': _default_line_modes, 'weight': 1},
        ('abcd', 'defg'): {'modes': _default_line_modes, 'weight': 1},
    }
}


def _test():
    test_data = dict(_test_data)
    import random

    for i in range(30):
        key = rand_key()
        for _ in range(random.choice(range(1)) + 1):
            connection = random.choice(test_data['nodes'].keys())
            if connection == key:
                continue
            import copy
            node_mode = copy.deepcopy(_default_node_modes)
            edge_mode = copy.deepcopy(_default_line_modes)
            color = [random.random() * 55, random.random() * 255, random.random() * 50, 255]
            node_mode['normal']['fill'] = color
            node_mode['normal']['pen'] = color
            node_mode['selected']['pen'] = [155, 155, 155, 255]
            node_mode['selected']['fill'] = [155, 155, 155, 255]
            node_mode['hover']['pen'] = [255, 255, 255, 255]
            node_mode['hover']['fill'] = [255, 255, 255, 255]
            edge_mode['normal']['pen'] = color
            edge_mode['hover']['pen'] = [255, 255, 255, 255]
            edge_mode['selected']['pen'] = [155, 155, 155, 255]

            test_data['nodes'][key] = {
                'name': 'Comma ,',
                'modes': node_mode,
                'tooltip': ','}
            test_data['connections'][(key, connection)] = {
                'modes': edge_mode,
                'weight': 30,
            }

    app = QApplication(sys.argv)
    w = NodeViewer(node_data=test_data)
    w.resize(450, 750)
    w.move(100, 100)
    w.setWindowTitle('Simple')
    w.showFullScreen()
    w.raise_()
    sys.exit(app.exec_())


def test():
    from . import dag
    digraph = dag.DiGraph()
    n = []

    clus = ['foo', 'bar']
    clus = ['foo']

    import random

    def random_key():
        nm = ""
        for _ in range(5):
            nm += random.choice('abcdefghijklmnopqrstuvwxyz')
        return nm

    for i in range(130):
        node_mode = {'normal': {}, 'selected': {}, 'hover': {}}
        color = [
            random.random() * 55,
            random.random() * 255,
            random.random() * 50,
            255]
        node_mode['normal']['fill'] = color
        node_mode['normal']['line_width'] = 1.5
        node_mode['normal']['pen'] = color
        node_mode['selected']['pen'] = [155, 155, 155, 255]
        node_mode['selected']['line_width'] = 1.5
        node_mode['selected']['fill'] = [155, 155, 155, 255]
        node_mode['hover']['pen'] = [255, 255, 255, 255]
        node_mode['hover']['line_width'] = 1.5
        node_mode['hover']['fill'] = [255, 255, 255, 255]
        k = dag.Node(
                random_key(),
                random.choice(clus),
                node_data={'modes': node_mode})
        digraph.add_node(k)
        n.append(k)

    for node in n:
        for i in range(random.choice(range(1)) + 1):
            color = node._node_data['modes']['normal']['fill']
            edge_mode = {'normal': {}, 'hover': {}, 'selected': {}}
            edge_mode['normal']['pen'] = color
            edge_mode['hover']['pen'] = [255, 255, 255, 255]
            edge_mode['selected']['pen'] = [155, 155, 155, 255]
            conn = random.choice(n)
            while node == conn:
                conn = random.choice(n)
            e = dag.Edge(node, conn, edge_data={'modes': edge_mode})
            digraph.add_edge(e)

    node_mode = {'normal': {}, 'selected': {}, 'hover': {}}
    color = [
        random.random() * 255,
        random.random() * 55,
        random.random() * 50,
        255]
    node_mode['normal']['fill'] = color
    node_mode['normal']['line_width'] = 1.5
    node_mode['normal']['pen'] = color
    node_mode['selected']['pen'] = [155, 155, 155, 255]
    node_mode['selected']['line_width'] = 1.5
    node_mode['selected']['fill'] = [155, 155, 155, 255]
    node_mode['hover']['pen'] = [255, 255, 255, 255]
    node_mode['hover']['line_width'] = 1.5
    node_mode['hover']['fill'] = [255, 255, 255, 255]

    b = dag.Box('sample_box', (125, 95),
                {'n': 3, 's': 2, 'w': 4, 'e': 5},
                random.choice(clus),
                box_data={'modes': node_mode})
    digraph.add_box(b)

    for i in range(3):
        e = dag.Edge(b.get_port('n', i), random.choice(n), 100)
        digraph.add_edge(e)

    color = [
        random.random() * 255,
        random.random() * 255,
        random.random() * 50,
        255]
    node_mode['normal']['fill'] = color
    node_mode['normal']['line_width'] = 1.5
    node_mode['normal']['pen'] = color
    node_mode['selected']['pen'] = [155, 155, 155, 255]
    node_mode['selected']['line_width'] = 1.5
    node_mode['selected']['fill'] = [155, 155, 155, 255]
    node_mode['hover']['pen'] = [255, 255, 255, 255]
    node_mode['hover']['line_width'] = 1.5
    node_mode['hover']['fill'] = [255, 255, 255, 255]
    b = dag.Box('sample_box2', (145, 335),
                {'n': 3, 's': 2, 'w': 4, 'e': 5},
                random.choice(clus),
                box_data={'modes': node_mode})
    digraph.add_box(b)

    for i in range(2):
        e = dag.Edge(b.get_port('e', 0), random.choice(n), 1000)
        digraph.add_edge(e)
    digraph.process_dot()

    app = QApplication(sys.argv)
    w = NodeViewer()
    w.set_node_data(digraph)
    w.resize(450, 750)
    w.move(100, 100)
    w.setWindowTitle('Simple')
    w.showFullScreen()
    w.raise_()
    sys.exit(app.exec_())
