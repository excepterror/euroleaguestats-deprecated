from kivy.uix.label import Label
from kivy.graphics import Color
from kivy.graphics.vertex_instructions import RoundedRectangle
from kivy.core.window import Window
from kivy.metrics import dp

scr_w = Window.system_size[0]
scr_h = Window.system_size[1]

factor1 = dp(38)
offset = (scr_w / 2 - 2 * factor1) / 1.5
a = 1.5 * factor1


class ToolTipTextUp(Label):

    """PURPOSE: Called by :meth: __init__ & on_touch_down in Class 'DraggableLogo' - main.py.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.font_size = '14sp'
        self.color = (1, .4, 0, .9)
        self.width = scr_w - 2 * offset
        self.height = '30dp'
        self.pos = (offset, scr_h - 2.7 * dp(40))

        with self.canvas.before:
            Color(1, 1, 1, .6)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, segments=40, radius=[10, ])
        self.bind(size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class ToolTipTextDown(Label):

    """PURPOSE: Called by :meth: __init__ & on_touch_down in Class 'DraggableLogo' - main.py.
    """

    def __init__(self):
        super().__init__()

        self.font_size = '14sp'
        self.color = (1, .4, 0, .9)
        self.width = scr_w - 2 * offset
        self.height = '30dp'
        self.pos = (offset, a + .6 * dp(40))

        with self.canvas.before:
            Color(1, 1, 1, .6)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, segments=40, radius=[10, ])
        self.bind(size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
