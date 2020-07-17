from kivy.graphics import Color, RoundedRectangle
from kivy.uix.label import Label
from kivy.uix.button import Button, ButtonBehavior


########################################################################################################################
# The following two Classes are used for the customisation of 'buttons' 'Enter' & 'Standings'.
########################################################################################################################


class AnotherSpecialButton(ButtonBehavior, Label):
    """This widget is practically an overlay to the widget below."""

    def __init__(self, **kwargs):
        super(AnotherSpecialButton, self).__init__(**kwargs)
        self.font_size = "21sp"
        self.color = [1, 1, 1, 1]
        self.halign = "center"
        self.valign = "middle"

        with self.canvas.before:
            Color(1, .2, 0, .9, mode='rgba')
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, segments=40, radius=[22, ])
        self.bind(size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class ASpecialButton(Label):
    """This widget serves as a background layer for the widget above."""

    def __init__(self, **kwargs):
        super(ASpecialButton, self).__init__(**kwargs)
        self.font_size = "21sp"
        self.color = [1, .2, 0, .9]  # It doesn't really matter what you enter here as long as alpha=0.
        self.halign = "center"
        self.valign = "middle"

        with self.canvas.before:
            Color(1, 1, 1, 1, mode='rgba')
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, segments=40, radius=[17, ])
        self.bind(size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class PlayerButton(Button):
    def __init__(self, **kwargs):
        super(PlayerButton, self).__init__(**kwargs)
        self.font_size = "16sp"
        self.color = [0, 0, 0, 1]
        self.background_normal = ""
        self.background_color = [1, 1, 1, .6]
        self.halign = "center"
        self.valign = "middle"

        self.bind(width=lambda *x: self.setter("text_size")(self, (self.width, None)))