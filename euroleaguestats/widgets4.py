from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics.vertex_instructions import RoundedRectangle


class DisplayLabel(Label):

    """Used in Class 'Roster' & 'Options' - main.py.
    """

    def __init__(self, r, g, b, a, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = [.94, .066]
        self.pos_hint = {'center_x': .5, 'y': .90}
        self.color = (1, 1, 1, 1)
        self.halign = 'center'
        self.valign = 'middle'
        self.markup = True

        self.r = r
        self.g = g
        self.b = b
        self.a = a

        with self.canvas.before:
            Color(r, g, b, a, mode='rgba')
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, segments=40, radius=[17, ])
        self.bind(size=self.update_rect)

        self.bind(width=lambda *x: self.setter('text_size')(self, (self.width, None)),
                  texture_size=lambda *x: self.setter('height')(self, self.texture_size[1]))

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class DisplayButton(Button):

    """Used in Class 'Roster' - main.py.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.font_size = '16sp'
        self.color = [0, 0, 0, 1]
        self.background_normal = ''
        self.background_color = [1, 1, 1, .6]
        self.halign = 'center'
        self.valign = 'middle'
        self.size_hint = [1, 1]

        self.bind(width=lambda *x: self.setter('text_size')(self, (self.width, None)))


class OptionsButtonLabel(ButtonBehavior, Label):

    """Used in Class 'Options' for button customisation - main.py.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = '17sp'
        self.color = [0, .6, .6, .8]
        self.halign = 'center'
        self.valign = 'middle'

        with self.canvas.before:
            Color(1, 1, 1, .6, mode='rgba')
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, segments=20, radius=[5, ])
        self.bind(size=self.update_rect)

        self.bind(width=lambda *x: self.setter("text_size")(self, (self.width, None)),
                  texture_size=lambda *x: self.setter("height")(self, self.texture_size[1]))

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
