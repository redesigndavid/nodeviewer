import sys
from PyQt4.QtGui import QApplication
from node_viewer import NodeViewer
from node_viewer import style
import random


_random_titles = [item.strip() for item in """
Back to the Future
Desperado
Night at the Museum
Robocop
Ghostbusters
Cool World
Donnie Darko
Double Indemnity
The Spanish Prisoner
The Smurfs
Dead Alive
Army of Darkness
Peter Pan
The Jungle Story
Red Planet
Deep Impact
The Long Kiss Goodnight
Juno
(500) Days of Summer
The Dark Knight
Bringing Down the House
Se7en
Chocolat
The American
The American President
Hudsucker Proxy
Conan the Barbarian
Shrek
The Fox and the Hound
Lock, Stock, and Two Barrels
Date Night
200 Cigarettes
9 1/2 Weeks
Iron Man 2
Tombstone
Young Guns
Fight Club
The Cell
The Unborn
Black Christmas
The Change-Up
The Last of the Mohicans
Shutter Island
Ronin
Ocean's 11
Philadelphia
Chariots of Fire
M*A*S*H
Walking and Talking
Walking Tall
The 40 Year Old Virgin
Superman III
The Hour
The Slums of Beverly Hills
Secretary
Secretariat
Pretty Woman
Sleepless in Seattle
The Iron Mask
Smoke
Schindler's List
The Beverly Hillbillies
The Ugly Truth
Bounty Hunter
Say Anything
8 Seconds
Metropolis
Indiana Jones and the Temple of Doom
Kramer vs. Kramer
The Manchurian Candidate
Raging Bull
Heat
About Schmidt
Re-Animator
Evolution
Gone in 60 Seconds
Wanted
The Man with One Red Shoe
The Jerk
Whip It
Spanking the Monkey
Steel Magnolias
Horton Hears a Who
Honey
Brazil
Gorillas in the Mist
Before Sunset
After Dark
From Dusk til Dawn
Cloudy with a Chance of Meatballs
Harvey
Mr. Smith Goes to Washington
L.A. Confidential
Little Miss Sunshine
The Future
Howard the Duck
Howard's End
The Innkeeper
Revolutionary Road
""".splitlines()]


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
    taken = []

    def random_title():
        key = None
        while not key or key in taken:
            key = random.choice(_random_titles)
        return key

    for i in range(90):
        color = [
            random.random() * 5,
            (random.random() * 150) + 55,
            random.random() * 10,
            255]
        k = dag.Node(random_title(), random.choice(clus), node_data={})
        k.style().set_attribute('fill_color', color, 'normal')
        k.style().set_attribute('pen_color', color, 'normal')
        k.style().set_attribute(
            'shape', random.choice(['rect', 'round']), '_all_states_')
        k.style().set_attribute(
            'size',
            [(random.random() * 5) + 15, (random.random() * 5) + 15],
            '_all_states_')
        digraph.add_node(k)
        n.append(k)

    for node in n:
        for i in range(random.choice(range(1)) + 1):
            color = node.style().get_value('fill_color', 'normal')
            conn = random.choice(n)
            while node == conn:
                conn = random.choice(n)
            e = dag.Edge(node, conn, edge_data={})
            e.style().set_attribute('fill_color', color, 'normal')
            e.style().set_attribute('pen_color', color, 'normal')
            e.style().set_attribute('arrow_width', 5 + (random.random() * 8), 'normal')
            e.style().set_attribute('line_width', 2 + (random.random() * 3), 'normal')
            digraph.add_edge(e)

    b = dag.Box('sample_box', (100, 150),
                {'n': 0, 's': 1, 'w': 3, 'e': 2},
                random.choice(clus),
                box_data={})
    color = [200, 200, 150, 255]
    b.style().set_attribute('fill_color',  color, 'normal')
    b.style().set_attribute('pen_color',  color, 'normal')
    b.style().set_attribute('label_alignment', 'above', '_all_states_')
    digraph.add_box(b)
    for port in b.get_ports():
        port.set_label(random_title())

    for i in range(3):
        e = dag.Edge(b.get_port('w', i), random.choice(n), 100)
        e.style().set_attribute('line_style', 'dash', style._all_states)
        e.style().set_attribute('pen_color', [251, 250, 250, 255], 'normal')
        digraph.add_edge(e)

    for i in range(2):
        e = dag.Edge(random.choice(n), random.choice(b.get_ports()))
        e.style().set_attribute('line_style', 'dot', style._all_states)
        e.style().set_attribute('pen_color', [251, 250, 250, 255], 'normal')
        digraph.add_edge(e)

    for i in range(2):
        e = dag.Edge(b.get_port('e', 0), random.choice(n))
        e.style().set_attribute('line_style', 'dot', style._all_states)
        e.style().set_attribute('pen_color', [250, 250, 250, 255], 'normal')
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
