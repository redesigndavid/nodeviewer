import sys
from PyQt4.QtGui import QApplication
from node_viewer import NodeViewer

_test_data = {
    'nodes': {
        'a': {'name': 'Asterisk *',
              'colors': {'default': (0, 250, 0, 255),
                         'line': (100, 10, 20, 255),
                         'hover': (255, 125, 0, 255),
                         'tooltip': (255, 125, 0, 255),
                         'click': (200, 200, 0, 255)},
              'tooltip': '*'},
        'b': {'name': 'Bang !',
              'colors': {'default': (255, 0, 0, 255),
                         'line': (100, 10, 20, 255),
                         'hover': (255, 125, 0, 255),
                         'tooltip': (255, 125, 0, 255),
                         'click': (200, 200, 0, 255)},
              'tooltip': '!'},
        'c': {'name': 'Comma ,',
              'colors': {'default': (255, 0, 255, 255),
                         'line': (100, 10, 20, 255),
                         'hover': (255, 125, 0, 255),
                         'tooltip': (255, 125, 0, 255),
                         'click': (200, 200, 0, 255)},
              'tooltip': ','},
        'a1': {'name': 'Asterisk *',
               'colors': {'default': (0, 250, 0, 255),
                          'line': (200, 10, 20, 255),
                          'hover': (255, 125, 0, 255),
                          'tooltip': (255, 125, 0, 255),
                          'click': (200, 200, 0, 255)},
               'tooltip': '*'},
        'b1': {'name': 'Bang !',
               'colors': {'default': (255, 0, 0, 255),
                          'line': (200, 10, 20, 255),
                          'hover': (255, 125, 0, 255),
                          'tooltip': (255, 125, 0, 255),
                          'click': (200, 200, 0, 255)},
               'tooltip': '!'},
        'c1': {'name': 'Comma ,',
               'colors': {'default': (255, 0, 255, 255),
                          'line': (200, 10, 20, 255),
                          'hover': (255, 125, 0, 255),
                          'tooltip': (255, 125, 0, 255),
                          'click': (200, 200, 0, 255)},
               'tooltip': ','},
        'a2': {'name': 'Asterisk *',
               'colors': {'default': (0, 250, 0, 255),
                          'line': (200, 10, 20, 255),
                          'hover': (255, 125, 0, 255),
                          'tooltip': (255, 125, 0, 255),
                          'click': (200, 200, 0, 255)},
               'tooltip': '*'},
        'b2': {'name': 'Bang !',
               'colors': {'default': (255, 0, 0, 255),
                          'line': (200, 10, 20, 255),
                          'hover': (255, 125, 0, 255),
                          'tooltip': (255, 125, 0, 255),
                          'click': (200, 200, 0, 255)},
               'tooltip': '!'},
        'c2': {'name': 'Comma ,',
               'colors': {'default': (255, 0, 255, 255),
                          'line': (200, 10, 20, 255),
                          'hover': (255, 125, 0, 255),
                          'tooltip': (255, 125, 0, 255),
                          'click': (200, 200, 0, 255)},
               'tooltip': ','},
        'a3': {'name': 'Asterisk *',
               'colors': {'default': (0, 250, 0, 255),
                          'line': (200, 10, 20, 255),
                          'hover': (255, 125, 0, 255),
                          'tooltip': (255, 125, 0, 255),
                          'click': (200, 200, 0, 255)},
               'tooltip': '*'},
        'b3': {'name': 'Bang !',
               'colors': {'default': (255, 0, 0, 255),
                          'line': (200, 10, 20, 255),
                          'hover': (255, 125, 0, 255),
                          'tooltip': (255, 125, 0, 255),
                          'click': (200, 200, 0, 255)},
               'tooltip': '!'},
        'c3': {'name': 'Comma ,',
               'colors': {'default': (255, 0, 255, 255),
                          'line': (200, 10, 20, 255),
                          'hover': (255, 125, 0, 255),
                          'tooltip': (255, 125, 0, 255),
                          'click': (200, 200, 0, 255)},
               'tooltip': ','},
    },
    'connections': [
        ('a', 'a1', ''),
        ('b', 'b1', ''),
        ('c', 'c1', ''),
        ('a', 'a2', ''),
        ('b', 'b2', ''),
        ('c', 'c2', ''),
        ('a2', 'a3', ''),
        ('b2', 'b3', ''),
        ('c2', 'c3', ''),
        ('a', 'b', ''),
        ('b', 'c', ''),
        ('c', 'a', ''),
    ]
}


def test():
    app = QApplication(sys.argv)
    #w = NodeViewer(node_data=_test_data)
    test_data = dict(_test_data)
    for i in range(40):
        import random
        key = str(random.random())
        connection = random.choice(test_data['nodes'].keys())
        test_data['nodes'][key] = {
            'name': 'Comma ,',
            'colors': {'default': (255 * random.random(), 255 * random.random(), 255 * random.random(), 255),
                       'line': (200 * random.random(), 10 * random.random(), 20 * random.random(), 255),
                       'hover': (255, 125, 0, 255),
                       'tooltip': (255, 125, 0, 255),
                       'click': (200, 200, 0, 255)},
            'tooltip': ','}
        test_data['connections'].append((key, connection, ''))
    w = NodeViewer(node_data=test_data)
    w.resize(450, 750)
    w.move(100, 100)
    w.setWindowTitle('Simple')
    w.show()
    sys.exit(app.exec_())
