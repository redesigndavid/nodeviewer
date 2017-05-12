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

    def get_value(self, attr_name, state):
        value = self._styles.get(attr_name, {}).get(state)
        if not value and self._defaults:
            value = self._defaults.get_value(attr_name, state)
        if not value:
            print attr_name, state
            value = _global_defaults.get(attr_name, state)
        return value

    def __repr__(self):
        import pprint
        d = dict(self._defaults and self._defaults._styles or {})
        s = dict(self._styles or {})
        d.update(s)
        return pprint.pformat(d)


class NodeStyle(Style):
    _defaults = Style()

    _defaults.set_attribute('fill_color', (255, 0, 0, 255), _all_states)
    _defaults.set_attribute('pen_color', (0, 0, 0, 255), _all_states)
    _defaults.set_attribute('line_width', 2, _all_states)

    _defaults.set_attribute('font_size', 10, _all_states)
    _defaults.set_attribute('font_color', (0, 0, 0, 255), _all_states)

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

