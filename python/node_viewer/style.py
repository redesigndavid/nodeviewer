import copy
_all_states = '_all_states_'
_states = [
    'normal', 'hover', 'selected',
    'click', 'inherit_selected',
    'consider_selection']

_global_defaults = {
    'node_fill_color': {
        'click': (255, 0, 0, 255),
        'hover': (255, 0, 0, 255),
        'normal': (255, 0, 0, 255),
        'selected': (255, 0, 0, 255)},
    'node_font_color': {
        'click': (0, 0, 0, 255),
        'hover': (0, 0, 0, 255),
        'normal': (0, 0, 0, 255),
        'selected': (0, 0, 0, 255)},
    'node_font_size': {
        'click': 10,
        'hover': 10,
        'normal': 10,
        'selected': 10},
    'node_line_width': {
        'click': 2,
        'hover': 2,
        'normal': 2,
        'selected': 2},
    'node_pen_color': {
        'click': (0, 0, 0, 255),
        'hover': (0, 0, 0, 255),
        'normal': (0, 0, 0, 255),
        'selected': (0, 0, 0, 255)}
}


class Style():
    _style_name = ''
    _defaults = None

    def __init__(self):
        if self._defaults:
            self._styles = copy.deepcopy(self._defaults._styles)
        else:
            self._styles = {}

    def set_attribute(self, attribute_name, value, state):
        if not state:
            return
        states = []
        if state == _all_states:
            states.extend(_states)
        elif isinstance(state, list):
            states.extend(state)
        elif isinstance(state, str):
            states.append(state)

        d = dict((state, value) for state in states)
        self._styles.setdefault(attribute_name, {}).update(d)

    def get_value(self, attr_name, state, default=None):
        value = self._styles.get(attr_name, {}).get(state)
        if not value and self._defaults:
            value = self._defaults.get_value(attr_name, state)
        if not value:
            value = _global_defaults.get(attr_name, default)
        return value

    def __repr__(self):
        import pprint
        d = dict(self._defaults and self._defaults._styles or {})
        s = dict(self._styles or {})
        d.update(s)
        return pprint.pformat(d)


class NodeStyle(Style):

    _defaults = Style()

    _defaults.set_attribute('shape', 'round', _all_states)
    _defaults.set_attribute('size', [10, 10], _all_states)

    _defaults.set_attribute('fill_color', (255, 0, 0, 255), _all_states)
    _defaults.set_attribute('pen_color', (255, 0, 0, 255), _all_states)
    _defaults.set_attribute('line_width', 2, _all_states)

    _defaults.set_attribute('font_size', 10, _all_states)
    _defaults.set_attribute('font_color', (0, 0, 0, 255), _all_states)

    _defaults.set_attribute('label_alignment', 'below', _all_states)
    _defaults.set_attribute('label_fill_color', (25, 125, 0, 255), _all_states)
    _defaults.set_attribute('label_font_color', (5, 25, 0, 255), _all_states)
    _defaults.set_attribute('label_pen_color', (25, 0, 0, 255), _all_states)
    _defaults.set_attribute('label_line_width', 1, _all_states)

    _defaults.set_attribute('label_alignment', 'above', 'selected')
    _defaults.set_attribute('label_fill_color', (125, 125, 0, 255), 'selected')
    _defaults.set_attribute('label_font_color', (0, 125, 0, 255), 'selected')
    _defaults.set_attribute('label_pen_color', (125, 125, 0, 255), 'selected')
    _defaults.set_attribute('label_line_width', 2, 'selected')

    _defaults.set_attribute(
        'fill_color', (255, 205, 205, 255),
        'consider_selection')
    _defaults.set_attribute(
        'pen_color', (255, 205, 205, 255),
        'consider_selection')

    _defaults.set_attribute('fill_color', (255, 255, 255, 255), 'selected')
    _defaults.set_attribute('pen_color', (255, 255, 255, 255), 'selected')

    _defaults.set_attribute('fill_color', (120, 255, 255, 255), 'hover')
    _defaults.set_attribute('pen_color', (120, 255, 255, 255), 'hover')

    _defaults.set_attribute('fill_color', (255, 255, 255, 255), 'click')
    _defaults.set_attribute('pen_color', (255, 255, 255, 255), 'click')


class BoxStyle(NodeStyle): pass


class GroupStyle(NodeStyle):

    _defaults = Style()
    _defaults.set_attribute('shape', 'round', _all_states)
    _defaults.set_attribute('size', [20, 20], _all_states)
    _defaults.set_attribute('peripheries', 1, _all_states)
    _defaults.set_attribute('fill_color', (255, 200, 0, 255), _all_states)
    _defaults.set_attribute('pen_color', (255, 100, 0, 255), _all_states)
    _defaults.set_attribute('line_width', 1, _all_states)

    _defaults.set_attribute('font_size', 10, _all_states)
    _defaults.set_attribute('font_color', (0, 0, 0, 255), _all_states)

    _defaults.set_attribute('label_alignment', 'below', _all_states)
    _defaults.set_attribute('label_fill_color', (25, 125, 0, 255), _all_states)
    _defaults.set_attribute('label_font_color', (5, 25, 0, 255), _all_states)
    _defaults.set_attribute('label_pen_color', (25, 0, 0, 255), _all_states)
    _defaults.set_attribute('label_line_width', 1, _all_states)
    _defaults.set_attribute('label_alignment', 'above', 'selected')
    _defaults.set_attribute('label_fill_color', (125, 125, 0, 255), 'selected')
    _defaults.set_attribute('label_font_color', (0, 125, 0, 255), 'selected')
    _defaults.set_attribute('label_pen_color', (125, 125, 0, 255), 'selected')
    _defaults.set_attribute('label_line_width', 2, 'selected')

    _defaults.set_attribute(
        'fill_color', (255, 205, 205, 255),
        'consider_selection')
    _defaults.set_attribute(
        'pen_color', (255, 205, 205, 255),
        'consider_selection')

    _defaults.set_attribute('fill_color', (255, 255, 255, 255), 'selected')
    _defaults.set_attribute('pen_color', (255, 255, 255, 255), 'selected')

    _defaults.set_attribute('fill_color', (120, 255, 255, 255), 'hover')
    _defaults.set_attribute('pen_color', (120, 255, 255, 255), 'hover')

    _defaults.set_attribute('fill_color', (255, 255, 255, 255), 'click')
    _defaults.set_attribute('pen_color', (255, 255, 255, 255), 'click')


class EdgeStyle(Style):

    _defaults = Style()

    _defaults.set_attribute('arrow_width', 8, _all_states)

    _defaults.set_attribute('pen_color', (0, 0, 0, 255), _all_states)
    _defaults.set_attribute('line_width', 2, _all_states)
    _defaults.set_attribute('pen_color', (0, 0, 0, 255), 'normal')
    _defaults.set_attribute('pen_color', (255, 255, 255, 255), 'selected')
    _defaults.set_attribute(
        'pen_color',
        (155, 155, 255, 255),
        'inherit_selected')
    _defaults.set_attribute(
        'pen_color', (255, 205, 205, 255),
        'consider_selection')

    _defaults.set_attribute('pen_color', (120, 255, 255, 255), 'hover')
    _defaults.set_attribute('pen_color', (255, 255, 255, 255), 'click')
    _defaults.set_attribute('line_style', 'solid', _all_states)
