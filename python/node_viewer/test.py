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
        'line_width': 1.8,
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
        'line_width': 2.5
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
        ('bcde', 'abcd'): {'modes': _default_line_modes, 'weight': 1},
        ('abcd', 'defg'): {'modes': _default_line_modes, 'weight': 1},
    }
}


def test():
    test_data = dict(_test_data)
    import random

    for i in range(130):
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
            edge_mode['normal']['pen'] = color
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
