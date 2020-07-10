from kivy.graphics import Color, RoundedRectangle
from kivy.uix.label import Label
from kivy.uix.button import ButtonBehavior


class AnyColorLabel(Label):

    """This widget is superimposed over the widget below."""

    def __init__(self, r, g, b, a, **kwargs):
        super().__init__(**kwargs)

        self.r = r
        self.g = g
        self.b = b
        self.a = a

        self.font_size = '21sp'

        self.color = (1, .2, 0, .8)
        self.halign = 'center'
        self.valign = 'middle'

        with self.canvas.before:
            Color(r, g, b, a)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, segments=70, radius=[60, ])
        self.bind(size=self.update_rect)

        self.bind(width=lambda *x: self.setter("text_size")(self, (self.width, None)),
                  texture_size=lambda *x: self.setter("height")(self, self.texture_size[1]))

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class AnyColorButton(ButtonBehavior, Label):

    """This widget serves as a background layer for the widget above."""

    def __init__(self, r, g, b, a, **kwargs):
        super().__init__(**kwargs)

        self.r = r
        self.g = g
        self.b = b
        self.a = a

        self.halign = 'center'
        self.valign = 'middle'

        with self.canvas.before:
            Color(r, g, b, a, mode='rgba')
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, segments=70, radius=[60, ])
        self.bind(size=self.update_rect)

        self.bind(width=lambda *x: self.setter("text_size")(self, (self.width, None)),
                  texture_size=lambda *x: self.setter("height")(self, self.texture_size[1]))

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
